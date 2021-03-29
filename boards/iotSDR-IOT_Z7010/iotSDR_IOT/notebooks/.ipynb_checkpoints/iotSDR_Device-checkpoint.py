

import iotFrontEndCore
import iotSDR_defs as defs
from pynq import MMIO
import pynq.lib.dma
from pynq import Xlnk
from pynq import Overlay

import numpy as np
import threading

import time
from queue import Queue 



class iotSDR():
    



    def __init__(self,overlay,args):
        
        """Bit file settings"""
        self.ol = overlay
        
        """Cache Settings"""
        self._cacheSampleRate = dict()
        self._cacheBandwidth  = dict()
        self._cacheFreq       = dict()
        self._cacheGain       = dict()
        self._checheTxLUT     = dict()
        
        """DMA bindings"""
        self.total_words = 2048
        #self.dma = self.ol.axi_dma_0
        #self.xlnk = Xlnk()
        #self.input_buffer = self.xlnk.cma_array(shape=(self.total_words,), dtype=np.uint32)
        
        """Initialize defs"""
        self.chA = self.createChannel(defs.chan_subGHz_A)
        self.chB = self.createChannel(defs.chan_subGHz_B)
    
        
        """Initialize DMA """
        self._dma_txrx_a = self.chA.pl_dma_recv
        self._dma_txrx_b = self.chB.pl_dma_recv
        
        
    """initialize transceiever"""
    def createChannel(self,chan):
        
        if chan == defs.chan_subGHz_A or \
           chan == defs.chan_24GHz_A:
            return iotFrontEndCore.Transceiver("ch1",self.ol)
        
        if chan == defs.chan_subGHz_B or \
           chan == defs.chan_24GHz_B:
            return iotFrontEndCore.Transceiver("ch2",self.ol)
        
        
    """
    
    Sample Rate API
    
    """
    def setSampleRate(self,direction,chan,rate):
        
        rate_act,val = self.adjustRate(rate)
        print("iotSDR Device: Requested rate: {}, Actual Rate: {:.2f} ".format(rate,rate_act))
        if direction == defs.IOTSDR_RX:
            
            if chan == defs.chan_subGHz_A:
                self.chA.setRxSampleRate(val,"subGHz")
            
            elif chan == defs.chan_24GHz_A:    
                self.chA.setRxSampleRate(val,"24GHz")
            
            elif chan == defs.chan_subGHz_B:
                self.chB.setRxSampleRate(val,"subGHz")
            
            elif chan == defs.chan_24GHz_B:    
                self.chB.setRxSampleRate(val,"24GHz")
            
            else:
                print("iotSDR Device: Channel is not correctly selected",chan)
                
        elif direction == defs.IOTSDR_TX:
            
            if chan == defs.chan_subGHz_A:
                self.chA.setRxSampleRate(val,"subGHz")
            
            elif chan == defs.chan_24GHz_A:    
                self.chA.setRxSampleRate(val,"24GHz")
            
            elif chan == defs.chan_subGHz_B:
                self.chB.setRxSampleRate(val,"subGHz")
            
            elif chan == defs.chan_24GHz_B:    
                self.chB.setRxSampleRate(val,"24GHz")
                        
            else:
                print("iotSDR Device: Channel is not correctly selected",chan)
        
        else:
                print("iotSDR Device: Diection is not correctly selected",direction)
                
        self._cacheSampleRate[direction,chan] = rate_act
        #self._cacheSampleRate[chan] = rate
        
        
    def getSampleRate(self,direction,chan):
        
        return self._cacheSampleRate.get((direction,chan))
    
    def listSampleRates(self,chan):
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
        # iot channels
        if chan < 4:
            return [4e6,
                    2e6,
                    round((4000/3)*1e3,2),
                    1e6,800e3,
                    round((2000/3)*1e3,2),
                    500e3,
                    400e3]
        
        # GPS channel
        if chan == 4:
            return  [4.092e6,16.368e6]
        
    def adjustRate(self,rate):
        if rate >= 4e6:
            return  4e6,0x1
        
        elif rate >=  2e6 and rate < 4e6:
            return 2e6,0x2
        
        elif rate >=  (4000/3)*1e3 and rate < 2e6:
            return round((4000/3)*1e3,2),0x3
        
        elif rate >=  1e6 and rate < (4000/3)*1e3:
            return 1e6,0x4
        
        elif rate >=  800e3 and rate < 1e6:
            return 800e3,0x5
        
        elif rate >=  (2000/3)*1e3 and rate < 800e3:
            return round((2000/3)*1e3,2),0x6
        
        elif rate >=  500e3 and rate < (2000/3)*1e3:
            return 500e3,0x8
        
        elif rate >=  400e3 and rate < 500e3:
            return 400e3,0xA
        
        else:
            return 4e6,0x1
        
    """
    
    Frequency Setting API
    
    """
    
    def setFrequency(self,chan,freq):
        
        
        freq_act = int(self.adjustFreq(freq,chan))
   
        if freq_act:
            if chan == defs.chan_subGHz_A:
                self.chA.txrx_frequency(5000,freq_act,11)

            elif chan == defs.chan_24GHz_A:    
                self.chA.txrx_frequency_24g(5000,freq_act,11)

            elif chan == defs.chan_subGHz_B:
                self.chB.txrx_frequency(5000,freq_act,11)

            elif chan == defs.chan_24GHz_B:    
                self.chB.txrx_frequency_24g(5000,freq_act,11)
                
            print("iotSDR Device: frequency:{} updated for channel:{}".format(freq_act,chan))    
                
            self._cacheFreq[chan] = freq        
        
    def getFrequency(self,chan):
        
        return self._cacheFreq.get(chan)
    
    
    def adjustFreq(self,freq,chan):
        """ 
        supported bands
        band1 = 389.5MHz …   510MHz
        band2 =   779MH  …   1020MHz
        band2 =  2400MHz …   2483.5MHz

        """
        if chan == defs.chan_subGHz_A or chan  == defs.chan_subGHz_B:
            if freq >=  389.5e6 and freq <= 510e6:
                return freq

            elif freq >  389.5e6 and freq < 779e6:
                print("iotSDR Device: frequency:{} not supported for channel:{}".format(freq,chan))
                return 0

            elif freq >= 779e6 and freq <= 1020e6:
                return freq

            else:
                print("iotSDR Device: frequency:{} not supported for channel:{}".format(freq,chan))
                return 0

        if chan == defs.chan_24GHz_A or chan == defs.chan_24GHz_B:   
            if freq >=  2400e6 and freq <= 2483.5e6:
                return freq

            else:
                print("iotSDR Device: frequency:{} not supported for channel:{}".format(freq,chan))
                return 0

            
    def listFrequencies(self,chan):
        freqBands = {"subGhzband" : ((389.5e6,510e6),(779e6,1020e6)),
                     "24Ghzband" : (2400e6,2483.5e6)
                    }
        if chan == defs.chan_subGHz_A or chan  == defs.chan_subGHz_B:
            return freqBands["subGhzband"]
        
        if chan == defs.chan_24GHz_A or chan == defs.chan_24GHz_B:
            return freqBands["24Ghzband"]
            
                
    """ 
    
    BW Filter API
    
    """
    
    def setBandwidth(self,direction,chan,bw):
        #radio_rx_bandwidth(self,bw)
        self._cacheBandwidth[direction,chan] = bw
    
    def getBandwidth(self,direction,chan):
    
        return self._cacheBandwidth.get((direction,chan))
    
    def listBandwidths(self,direction):
        pass
        
        if direction == IOTSDR_RX:
            """
            0x0 fBW=160kHz;  fIF=250kHz
            0x1 fBW=200kHz;  fIF=250kHz
            0x2 fBW=250kHz;  fIF=250kHz
            0x3 fBW=320kHz;  fIF=500kHz
            0x4 fBW=400kHz;  fIF=500kHz
            0x5 fBW=500kHz;  fIF=500kHz
            0x6 fBW=630kHz;  fIF=1000kHz
            0x7 fBW=800kHz;  fIF=1000kHz
            0x8 fBW=1000kHz; fIF=1000kHz
            0x9 fBW=1250kHz; fIF=2000kHz
            0xA fBW=1600kHz; fIF=2000kHz
            0xB fBW=2000kHz; fIF=2000kHz
            """
            pass
        
        if direction == IOTSDR_TX:
            pass
    
    """
    
    Gain Setting API
    
    """
    
    def setGain(self,chan,gain):
        
        gain_adj = 0 if gain < 0 else 31 if gain > 31 else gain
        
        if chan == defs.chan_subGHz_A:
            self.chA.radio_tx_power(gain_adj)

        elif chan == defs.chan_24GHz_A:    
            self.chA.radio_tx_power_24g(gain_adj)

        elif chan == defs.chan_subGHz_B:
            self.chB.radio_tx_power(gain_adj)

        elif chan == defs.chan_24GHz_B:    
            self.chB.radio_tx_power_24g(gain_adj)
                
        print("iotSDR Device: Gain:{} updated for channel:{}".format(gain_adj,chan))    
                
        self._cacheGain[chan] = gain_adj
        
    def getGain(self,chan):
        
        return self._cacheGain.get(chan)
        
    def getGainRange(self,chan):
        
        return (0,31)
    
    
    """
    
    tramsmitter Fixed IQ LUT API
    
    """
    
    def setTxLUT(self,chan,IQsamples):
        
        if chan == defs.chan_subGHz_A or chan == defs.chan_24GHz_A:
            self.chA.set_tx_LUT(IQsamples)
            
        elif chan == defs.chan_subGHz_B or chan == defs.chan_24GHz_B:    
            self.chB.set_tx_LUT(IQsamples)
            
        self._checheTxLUT[chan] = IQsamples      
        
    
    def getTxLUT(self,chan):
        
        return self._checheTxLUT[chan]