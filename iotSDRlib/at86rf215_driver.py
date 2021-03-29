# Copyright (c) 2020, embedINN
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Radio driver for the AT86RF215
\ author Jonathan Munoz (jonathan.munoz@inria.fr), January 2017.
"""

import threading
import time
import logging
import sys

import spidev

import iotSDR.at86rf215_defs as defs

RADIOSTATE_RFOFF = 0x00  # ///< Completely stopped.
RADIOSTATE_FREQUENCY_SET = 0x01  # ///< Listening for commands, but RF chain is off.
RADIOSTATE_PACKET_LOADED = 0x02  # ///< Configuring the frequency.
RADIOSTATE_TRX_ENABLED = 0x03  # ///< Done configuring the frequency.
RADIOSTATE_RECEIVING = 0x04  # ///< Loading packet into the radio's TX buffer.
RADIOSTATE_TXRX_DONE = 0x05  # ///< Packet is fully loaded in the radio's TX buffer.

MODEM_SUB_GHZ       = 0
MODEM_2GHZ          = 1


class At86rf215(object):

    def __init__(self, cb, modem_base_band_state, SPIchannel):

        # store params
        self.cb                     = cb

        # local variables
        self.at86_state             = RADIOSTATE_RFOFF
        self.spi                    = spidev.SpiDev()
        self.state_trx_prep         = threading.Event()
        self.state_tx_now           = threading.Event()
        self.state_IFS              = threading.Event()
        self.state_reset            = threading.Event()
        self.dataLock               = threading.RLock()
        self.count                  = 0
        self.counter                = 0
        self.toggle_LED             = False
        self.f_reset_button         = False
        self.f_reset_pin            = False
        self.modem_base_band_state  = MODEM_SUB_GHZ

        self.state              = {'state_TRXprep': self.state_trx_prep, 'state_TXnow': self.state_tx_now,
                                   'state_RF_reset': self.state_reset}

        self.state['state_TRXprep'].clear()
        self.state['state_TXnow'].clear()
        self.state['state_RF_reset'].clear()
        
        self.SPIchannel                = SPIchannel

    # ======================== public ==========================================

    # ======================== private =========================================

    def read_isr_source(self):
        """
        Read the interruption source from the radio.

        This function is called typically after the interrupt pin triggers.
        The CPU then called this function the read the 4 RG_RFXX_IRQS registers
        to figure out the reason for the interrupt.

        FIXME: document parameter "channel"
        """
        # now = time.time()
        isr = self.radio_read_spi(defs.RG_RF09_IRQS, 4)
        if isr[0] & defs.IRQS_WAKEUP:
            self.at86_state = RADIOSTATE_RFOFF
            with self.dataLock:
                self.state['state_RF_reset'].set()

        if isr[0] & defs.IRQS_TRXRDY_MASK:
            self.at86_state = RADIOSTATE_TRX_ENABLED
            with self.dataLock:
                self.state['state_TRXprep'].set()

        if isr[1] & defs.IRQS_WAKEUP:                   # 2.4 GHZ
            self.at86_state = RADIOSTATE_RFOFF
            with self.dataLock:
                self.state['state_RF_reset'].set()

        if isr[1] & defs.IRQS_TRXRDY_MASK:              # 2.4 GHZ
            self.at86_state = RADIOSTATE_TRX_ENABLED
            with self.dataLock:
                self.state['state_TRXprep'].set()

        if isr[2] & defs.IRQS_TXFE_MASK:
            self.at86_state = RADIOSTATE_TXRX_DONE
            with self.dataLock:
                self.state['state_TXnow'].set()
            self.count += 1

        if isr[2] & defs.IRQS_RXFE_MASK:
            self.count += 1
            self.at86_state = RADIOSTATE_TXRX_DONE
            self.modem_base_band_state = MODEM_SUB_GHZ
            (pkt_rcv, rssi, crc, mcs) = self.radio_get_received_frame()
            self.cb(pkt_rcv, rssi, crc, mcs)

        if isr[3] & defs.IRQS_TXFE_MASK:                # 2.4 GHZ
            self.at86_state = RADIOSTATE_TXRX_DONE
            with self.dataLock:
                self.state['state_TXnow'].set()
            self.count += 1

        if isr[3] & defs.IRQS_RXFE_MASK:                # 2.4 GHZ
            self.count += 1
            self.at86_state = RADIOSTATE_TXRX_DONE
            self.modem_base_band_state = MODEM_2GHZ
            (pkt_rcv, rssi, crc, mcs) = self.radio_get_received_frame_2_4ghz()
            self.cb(pkt_rcv, rssi, crc, mcs)

    def radio_base_band_mode(self):
        return self.modem_base_band_state

    def cb_radio_isr(self, channel = 11):
        self.read_isr_source()

    def spi_init(self):
        """
        Initialize the SPI modules.
        :return: nothing
        """
        self.spi.open(self.SPIchannel, 0)
        #self.spi.open(2, 0)
        self.spi.max_speed_hz = 7800000

    def radio_probe(self):
        """
        probe the SPI, get chip id.
        :return: chip_id
        """
        return self.radio_read_spi(defs.RG_RF_PN, 1) 
        
    def radio_reset(self):
        """
        It reset the radio.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF_RST, defs.RST_CMD)
        #self.state['state_RF_reset'].wait()
        #self.state['state_RF_reset'].clear()

    def radio_set_frequency(self, channel_set_up):
        """
        # channel_spacing in kHz
        # frequency_0 in kHz
        # channel number
        # def set_frequency(channel_spacing, frequency_0, channel):
        """
        frequency_0 = channel_set_up[1] // 25
        self.radio_write_spi(defs.RG_RF09_CS, channel_set_up[0] // 25)
        self.radio_write_spi(defs.RG_RF09_CCF0L, frequency_0 & 0xFF)
        self.radio_write_spi(defs.RG_RF09_CCF0H, frequency_0 >> 8)
        self.radio_write_spi(defs.RG_RF09_CNL, channel_set_up[2] & 0xFF)
        self.radio_write_spi(defs.RG_RF09_CNM, channel_set_up[2] >> 8)

    def radio_set_frequency_2_4ghz(self, channel_set_up):
        """
        # channel_spacing in kHz
        # frequency_0 in kHz
        # channel number
        # def set_frequency(channel_spacing, frequency_0, channel):
        """
        frequency_0 = (channel_set_up[1]-1500000) // 25
        self.radio_write_spi(defs.RG_RF24_CS, channel_set_up[0] // 25)
        self.radio_write_spi(defs.RG_RF24_CCF0L, frequency_0 & 0xFF)
        self.radio_write_spi(defs.RG_RF24_CCF0H, frequency_0 >> 8)
        self.radio_write_spi(defs.RG_RF24_CNL, channel_set_up[2] & 0xFF)
        self.radio_write_spi(defs.RG_RF24_CNM, channel_set_up[2] >> 8)

    # FIXME: rename to radio_off
    def radio_off(self):
        """
        Puts the radio in the TRXOFF mode.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF09_CMD, defs.CMD_RF_TRXOFF)
        # self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_SLEEP)

    def radio_off_24(self):
        """
        Puts the radio in the TRXOFF mode.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_TRXOFF)
        # self.radio_write_spi(defs.RG_RF09_CMD, defs.CMD_RF_SLEEP)

    # TX
    def radio_load_packet(self, packet, CRC_SIZE):
        """
        Sends a packet to the buffer of the radio.
        :param packet: the packet to be sent.
        :return: Nothing
        """
        # send the size of the packet + size of the CRC (4 bytes)
        fifo_tx_len = defs.RG_BBC0_TXFLL[:] + [((len(packet) + CRC_SIZE) & 0xFF), (((len(packet) + CRC_SIZE) >> 8) & 0x07)]
        fifo_tx_len[0] |= 0x80
        self.radio_write_spi(fifo_tx_len)
        # send the packet to the modem tx fifo
        frame = defs.RG_BBC0_FBTXS[:] + packet
        frame[0] |= 0x80
        self.radio_write_spi(frame)

    def radio_load_packet_2_4ghz(self, packet, CRC_SIZE):
        """
        Sends a packet to the buffer of the radio.
        :param packet: the packet to be sent.
        :return: Nothing
        """
        # send the size of the packet + size of the CRC (4 bytes)
        fifo_tx_len = defs.RG_BBC1_TXFLL[:] + [((len(packet) + CRC_SIZE) & 0xFF), (((len(packet) + CRC_SIZE) >> 8) & 0x07)]
        fifo_tx_len[0] |= 0x80
        self.radio_write_spi(fifo_tx_len)
        # send the packet to the modem tx fifo
        frame = defs.RG_BBC1_FBTXS[:] + packet
        frame[0] |= 0x80
        self.radio_write_spi(frame)

    def radio_trx_enable(self):
        """
        Puts the radio in the TRXPREP, previous state to send/receive. It waits until receives a signal from the radio.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF09_CMD, defs.CMD_RF_TXPREP)
        #self.state['state_TRXprep'].wait()
        #self.state['state_TRXprep'].clear()

    def radio_trx_24_enable(self):
        """
        Puts the radio in the TRXPREP, previous state to send/receive. It waits until receives a signal from the radio.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_TXPREP)
        
    def radio_iq_enable(self):
        """
        Puts the radio in the IQ radio Mode, 
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF_IQIFC1, defs.CMD_RF_IQ_MODE)
    
    def radio_tx_now(self):
        """
        Commands the radio to send a previous loaded packet. It waits until the radio confirms the success.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF09_CMD, defs.CMD_RF_TX)
        # TODO: foreseen the case when there is a failure in the tx -TXRERR.
        #self.state['state_TXnow'].wait()
        #self.state['state_TXnow'].clear()

    def radio_tx_24_now(self):
        """
        Commands the radio to send a previous loaded packet. It waits until the radio confirms the success.
        :return: Nothing
        """
        self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_TX)
        # TODO: foreseen the case when there is a failure in the tx -TXRERR.
        #self.state['state_TXnow'].wait()
        #self.state['state_TXnow'].clear()

    # RX
    def radio_rx_now(self):
        """
        Puts the radio in reception mode, listening for frames.
        :return:
        """
        self.radio_write_spi(defs.RG_RF09_CMD, defs.CMD_RF_RX)

    def radio_rx_24_now(self):
        """
        Puts the radio in reception mode, listening for frames.
        :return:
        """
        self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_RX)
   
    def radio_rx_bandwidth(self,bandwidth):
        """
        Sets Radio front end filter bandwidth.
        :return:
        """
        self.radio_write_spi(defs.RG_RF09_RXBWC, 0x0)
        self.radio_write_spi(defs.RG_RF09_RXBWC, bandwidth)

    def radio_rx_config_frontEnd(self,cutOff,sampleRate):
        """
        sets cutoff frequency, 
        0x0     fCUT=0.25 *fS/2
        0x1     fCUT=0.375*fS/2
        0x2     fCUT=0.5 *fS/2
        0x3     fCUT=0.75 *fS/2
        0x4     fCUT=1.00 *fS/2
        :return:
        """
        self.radio_write_spi(defs.RG_RF09_RXDFE, cutOff << 5 | sampleRate)

    def radio_rx_agc(self,enable):
        """
        Sets the  AGC enable/disable.
        :return:
        """
        self.radio_write_spi(defs.RG_RF09_AGCC, enable)

    def radio_rx_agc_gain(self,target,gain):
        """
        Puts the radio in reception mode, listening for frames.
        :return:
        """
        self.radio_write_spi(defs.RG_RF09_AGCS, 0x0 )
        self.radio_write_spi(defs.RG_RF09_AGCS,target << 5 | gain )

    def radio_rx_now_2_4ghz(self):
        """
        Puts the radio in reception mode, listening for frames.
        :return:
        """
        self.radio_write_spi(defs.RG_RF24_CMD, defs.CMD_RF_RX)

    def radio_get_received_frame(self):
        """
        Demands to the radio the received packet
        :return: a tuple with 1) packet received, 2) rssi, 3) crc(boolean) 4) mcs (valid for OFDM).
        """
        # get the length of the received frame
        rcv = self.radio_read_spi(defs.RG_BBC0_RXFLL, 2)
        len_frame = rcv[0] + ((rcv[1] & 0x07) << 8)

        # read the packet
        frame_rcv = self.radio_read_spi(defs.RG_BBC0_FBRXS, len_frame)
        # logging.debug('frame number: {0}'.format(frame_rcv[0:2]))
        # read from metadata
        rssi = self.radio_read_spi(defs.RG_RF09_EDV, 1)[0]
        crc = ((self.radio_read_spi(defs.RG_BBC0_PC, 1))[0] >> 5) & 0x01
        mcs = self.radio_read_spi(defs.RG_BBC0_OFDMPHRRX, 1)[0] & defs.OFDMPHRRX_MCS_MASK

        # representing the RSSI value in dBm
        if rssi == 127:
            rssi = 'not valid'

        if rssi >= 128:
            rssi = (((~rssi) & 0xFF) + 1) * -1

        return frame_rcv, rssi, crc, mcs

    def radio_get_received_frame_2_4ghz(self):
        """
        Demands to the radio the received packet
        :return: a tuple with 1) packet received, 2) rssi, 3) crc(boolean) 4) mcs (valid for OFDM).
        """
        # get the length of the received frame
        rcv = self.radio_read_spi(defs.RG_BBC1_RXFLL, 2)
        len_frame = rcv[0] + ((rcv[1] & 0x07) << 8)

        # read the packet
        frame_rcv = self.radio_read_spi(defs.RG_BBC1_FBRXS, len_frame)
        # logging.debug('frame number: {0}'.format(frame_rcv[0:2]))
        # read from metadata
        rssi = self.radio_read_spi(defs.RG_RF24_EDV, 1)[0]
        crc = ((self.radio_read_spi(defs.RG_BBC1_PC, 1))[0] >> 5) & 0x01
        mcs = self.radio_read_spi(defs.RG_BBC1_OFDMPHRRX, 1)[0] & defs.OFDMPHRRX_MCS_MASK
        # mcs = 0
        # representing the RSSI value in dBm
        if rssi == 127:
            rssi = 'not valid'

        if rssi >= 128:
            rssi = (((~rssi) & 0xFF) + 1) * -1

        return frame_rcv, rssi, crc, mcs

    def radio_write_config(self, settings):
        """
        It writes a given configuration to the radio, contained in the list of tuples passed as parameters.
        :param settings: a list of tuples containing the address of the registers [0] and the value to write [1]
        :return: nothing
        """
        for reg in settings:
            self.radio_write_spi(reg[0], reg[1])

    def radio_read_spi(self, address, nb_bytes):
        """
        It gets a value or values of the registers starting at the address given.
        :param address: the register to be read
        :param nb_bytes: the amount of bytes to read starting at that address
        :return: the value(s) of the register(s)
        """
        reg = address[:]
        reg += [0x00] * nb_bytes
        data = self.spi.xfer2(reg)
        return data[2:]

    def radio_write_spi(self, address, value=None):
        """
        It writes a value to a register.
        :param address: the register to be written
        :param value: the value to be written
        :return: nothing
        """
        reg = address[:]
        if value is not None:
            reg = address[:] + [value]
        reg[0] |= 0x80
        self.spi.xfer2(reg)

    def check_radio_state_rf09(self):
        """
        It reads the radio state value
        :return: that read value
        """
        add = defs.RG_RF09_STATE[:] + [0x00]
        return self.spi.xfer2(add)[2]

    def check_radio_state_rf24(self):
        """
        It reads the radio state value
        :return: that read value
        """
        add = defs.RG_RF24_STATE[:] + [0x00]
        return self.spi.xfer2(add)[2]











