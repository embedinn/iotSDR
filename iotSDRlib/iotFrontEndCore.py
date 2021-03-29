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

import iotSDR.at86rf215_driver as radio
import iotSDR.at86rf215_defs as defs
from pynq import MMIO

import numpy as np

class Transceiver(object):
    """This class is used for the radio/pl/ps settings"""
    
    def __init__(self,channel='ch1',overlay=None):
        
        self.channel = channel
        self.overlay  = overlay
        self._radio_init(self.channel)
        self._pl_cores_init(self.channel)

        #self.rxtx_lvds_reset(self.channel)
    
    def _radio_init(self,channel):
        """channel: at86rf215 chip selection"""
        
        self.spidev = 2 if channel == 'ch2' else 1
            
        self.radio = radio.At86rf215(0,0,self.spidev)
        self.radio.spi_init()
        self.radio.radio_reset()
        
        #Configure RFCHIP as IQ samples
        """FIXME:Sample Rate is fixed in PL"""
        """FIXME:lvds ddr delay caliberation"""
        sample_rate = 2
        ddrDelay = 1
        self.radio.radio_write_spi(defs.RG_RF_IQIFC1,0x1 << 4 | ddrDelay)
        self.radio.radio_write_spi(defs.RG_RF09_RXDFE,sample_rate)
        self.radio.radio_write_spi(defs.RG_RF_IQIFC0,0x34)
        self.radio.radio_trx_enable()
        self.radio.radio_trx_24_enable()
        
        self.radio_ddr_delay(3)
        
    def setTxSampleRate(self,rate,chan):
        """
        0x1 fS = 4000kHz
        0x2 fS = 2000kHz
        0x3 fS = (4000/3)kHz
        0x4 fS = 1000kHz
        0x5 fS = 800kHz
        0x6 fS = (2000/3)kHz
        0x8 fS = 500kHz
        0xA fS = 400kHz
        """
        #FIXME:Sample rate support in Pl
        defaultRate = rate
        if chan == "subGHz":
            self.radio.radio_write_spi(defs.RG_RF09_TXDFE,defaultRate)
            
        if chan == "24GHz":
            self.radio.radio_write_spi(defs.RG_RF24_TXDFE,defaultRate)
            
        
    def setRxSampleRate(self,rate,chan):
        """
        0x1 fS = 4000kHz
        0x2 fS = 2000kHz
        0x3 fS = (4000/3)kHz
        0x4 fS = 1000kHz
        0x5 fS = 800kHz
        0x6 fS = (2000/3)kHz
        0x8 fS = 500kHz
        0xA fS = 400kHz
        """
        #FIXME:Sample rate support in Pl
        defaultRate = rate
        if chan == "subGHz":
            self.radio.radio_write_spi(defs.RG_RF09_RXDFE,defaultRate)
            
        if chan == "24GHz":
            self.radio.radio_write_spi(defs.RG_RF24_RXDFE,defaultRate)
            
            
    def radio_ddr_delay(self,delay):
        """Delay = 0,1,2,3"""
        self.radio.radio_write_spi(defs.RG_RF_IQIFC1,0x1 << 4 | delay)
        
    def radio_start_reception(self,chan):
        if chan == "subGHz":
            self.radio.radio_trx_enable()
            self.radio.radio_rx_now()
        if chan == "24GHz":
            self.radio.radio_trx_24_enable()
            self.radio.radio_rx_24_now()
        
    def radio_start_transmission(self,chan):
        if chan == "subGHz":
            self.radio.radio_trx_enable()
            self.radio.radio_tx_now()
        if chan == "24GHz":
            self.radio.radio_trx_24_enable()
            self.radio.radio_tx_24_now()
    
    def radio_prep_mode(self):
        self.radio.radio_trx_enable()
   
    def radio_loopback(self):
        self.radio.radio_write_spi(defs.RG_RF_IQIFC0,0x34)

    def radio_tx_power(self,val=28):
        self.radio.radio_write_spi(defs.RG_RF09_PAC,val)
        
    def radio_tx_power_24g(self,val=28):
        self.radio.radio_write_spi(defs.RG_RF24_PAC,val)    
    
    def txrx_frequency(self,
        channel_spacing_kHz = 25,
        frequency_0_kHz = 850000,
        channel = 11
        ):

        channel_set_up = (channel_spacing_kHz, frequency_0_kHz, channel)
        self.radio.radio_set_frequency(channel_set_up)

    def txrx_frequency_24g(self,
        channel_spacing_kHz = 5000,
        frequency_0_kHz = 850000,
        channel = 11
        ):

        channel_set_up = (channel_spacing_kHz, frequency_0_kHz, channel)
        self.radio.radio_set_frequency_2_4ghz(channel_set_up)

    """PL Side Methods"""

    def _pl_cores_init(self,channel):

        self.ADDRESS_RANGE  = 0x1000
        self.ADDRESS_OFFSET = 0x00
        
        #RX IP bit offset settings
        self.IQENABLE_OFFSET    = 8
        self.FIFORESET_OFFSET   = 4
        self.LVDSRESET_OFFSET   = 12
        self.IQSTREAMSEL_OFFSET = 0

        #TX IP bit offset settings
        self.BRAM_ADDR_RANGE       = 4096
        self.EN_BRAM_STREAM_OFFSET = 0
        self.ADDRESS_RESET_OFFSET  = 1
        self.TX_SAMPLE_RATE_OFFSET = 4
    
        """PL IP cores Addresses"""
        if (self.channel == 'ch1'):
            RECEIVER_SETTINGS_ADDRESS     = 0x41200000
            SAMPLESPERBLOCK_ADDRESS       = 0x41210000
            TRANSMITTER_IQ_BRAM_ADDRESS   = 0x42000000
            TRANSMITTER_SETTINGS_ADDRESS  = 0x41230000
            self.TxSettings   = MMIO(TRANSMITTER_SETTINGS_ADDRESS, 0x4)
            self.IQStreamBram = MMIO(TRANSMITTER_IQ_BRAM_ADDRESS, self.BRAM_ADDR_RANGE)
            self.RxSettings   = MMIO(RECEIVER_SETTINGS_ADDRESS, 0x4)
            self.BlockSizeReg = MMIO(SAMPLESPERBLOCK_ADDRESS, self.ADDRESS_RANGE)
            self.pl_dma_txrx  = self.overlay.TRX_CH1.axi_dma_txrx_09
        else:
            RECEIVER_SETTINGS_ADDRESS     = 0x41240000
            SAMPLESPERBLOCK_ADDRESS       = 0x41220000
            TRANSMITTER_IQ_BRAM_ADDRESS   = 0x40000000
            TRANSMITTER_SETTINGS_ADDRESS  = 0x41250000
            self.TxSettings   = MMIO(TRANSMITTER_SETTINGS_ADDRESS, 0x4)
            self.IQStreamBram = MMIO(TRANSMITTER_IQ_BRAM_ADDRESS, self.BRAM_ADDR_RANGE)
            self.RxSettings   = MMIO(RECEIVER_SETTINGS_ADDRESS, 0x4)
            self.BlockSizeReg = MMIO(SAMPLESPERBLOCK_ADDRESS, self.ADDRESS_RANGE)
            self.pl_dma_txrx  = self.overlay.TRX_CH2.axi_dma_txrx_09

    def rx_samples_select(self,source=2):
        """
        source =
        enable_tx_loopback = 0x0
        eanble_rf_09       = 0x1
        eanble_rf_24       = 0x2
        """
        #bit 0-1
        mask = self.RxSettings.read(0) & 0xFFFFFFFC
        self.RxSettings.write(0, source | mask)
    
    def enable_pl_rx_samples(self,val):
        #bit 8
        mask = self.RxSettings.read(0) & 0xFFFFFEFF 
        self.RxSettings.write(0, val  << 8 | mask)

    def tx_samples_select(self,source=1):
        # bit 0
        mask = self.TxSettings.read(0) & 0xFFFFFFFE
        self.TxSettings.write(0x0, source | mask )


    def set_rx_block_size(self,samples_size=1024):
        self.BlockSizeReg.write(0, samples_size)
    
    def rx_fifo_reset(self):
        # bit 4
        mask = self.RxSettings.read(0) & 0xFFFFFFF7
        self.RxSettings.write(0, 0x1 << 4 | mask)
        self.RxSettings.write(0, 0x0 << 4 | mask)

    def rxtx_lvds_reset(self):
        # bit 12
        mask = self.RxSettings.read(0) & 0xFFFFFFF7
        self.RxSettings.write(0, 0x1 << 12 | mask)
        self.RxSettings.write(0, 0x0 << 12 | mask)

    def enable_buffer_tx_samples(self,val):
        #FIXME: Seperate enable and source  sel
        # bit 0
        mask = self.TxSettings.read(0) & 0xFFFFFFFE
        self.TxSettings.write(0x0, val | mask )

        
    
    def set_tx_LUT(self,IQsamples,chan):
        
        self.Isamples  = np.array(IQsamples.real*(2**13-1),dtype=np.int16)
        self.Qsamples  = np.array(IQsamples.imag*(2**13-1),dtype=np.int16)
        #print("Core:",(IQsamples)) 
        j = 0
        for bramAdress in range(0,len(self.Isamples)*4,4):
                y = ((int(self.Isamples[j]) << 16) & 0xFFFFFFFF | int(self.Qsamples[j]) & 0xFFFF) &  0xFFFFFFFF
                self.IQStreamBram.write(bramAdress,y)
                j+=1

        self.enable_buffer_tx_samples(1)
        self.radio_start_transmission(chan)
        
    def set_tx_LUT_remote(self,IQsamples):
        
        #self.radio.radio_reset()
        
        self.Isamples  = np.array(IQsamples.real)#*(2**13-1),dtype=np.int16)
        self.Qsamples  = np.array(IQsamples.imag)#*(2**13-1),dtype=np.int16)
        #print("Core:",(IQsamples)) 
        j = 0
        for bramAdress in range(0,len(self.Isamples)*4,4):
                y = ((int(self.Isamples[j]) << 16) & 0xFFFFFFFF | int(self.Qsamples[j]) & 0xFFFF) &  0xFFFFFFFF
                self.IQStreamBram.write(bramAdress,y)
                j+=1

        self.enable_buffer_tx_samples(1)
        self.radio_start_transmission(chan)