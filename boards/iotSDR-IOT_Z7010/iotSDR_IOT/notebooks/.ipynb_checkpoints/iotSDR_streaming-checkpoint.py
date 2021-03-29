
import numpy as np
import iotSDR_Device as iotSDR
import iotSDR_defs as defs

from pynq import Xlnk
import acquiareDmaSamples as rx_streamer


class iotSDR_stream(iotSDR.iotSDR):

    
    def __init__(self,overlay,args):
        super().__init__(overlay,args)    
        
        
        self.xlnk = Xlnk()
    
    def setupStream(self,direction,channel):
        self.direction  = direction
        self.channel    = channel
        
        
        if direction == defs.IOTSDR_TX:
            if self.channel == defs.chan_subGHz_A:
                rawstream = rx_streamer.RawIQSamples(self.chA,1,1024)
                
                self._tx_samples_buffer = self.xlnk.cma_array(shape=(defs.SAMPLE_BLK_SIZE,), dtype=np.int32)
                print("iotSDR Device: Channel: chan_subGHz_A stream setup ")
                return (self._dma_txrx_a,self._tx_samples_buffer)
                
            elif self.channel == defs.chan_subGHz_B:
                
                self.tx_sample_buffer = self.xlnk.cma_array(shape=(defs.SAMPLE_BLK_SIZE,), dtype=np.int32)
                print("iotSDR Device: Channel: chan_subGHz_B stream setup ")
                return (self._dma_txrx_b,self.tx_sample_buffer)
                
            else:
                print("iotSDR Device: Channel is not selected correctly")
                
        if direction == defs.IOTSDR_RX:
            if self.channel == defs.chan_subGHz_A:
                self.chA.rx_samples_select(1)
                self.rawstream = rx_streamer.RawIQSamples(self.chA,1,defs.SAMPLE_BLK_SIZE)
                self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_A stream setup ")
                return self.rawstream
            
            elif self.channel == defs.chan_subGHz_B:
                self.chA.rx_samples_select(1)
                self.rawstream = rx_streamer.RawIQSamples(self.chB,1,defs.SAMPLE_BLK_SIZE)
                self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_A stream setup ")
                return self.rawstream

            elif self.channel == defs.chan_24GHz_A:
                self.chA.rx_samples_select(2)
                self.rawstream = rx_streamer.RawIQSamples(self.chA,1,defs.SAMPLE_BLK_SIZE)
                self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_A stream setup ")
                return self.rawstream

            elif self.channel == defs.chan_24GHz_B:
                self.chB.rx_samples_select(2)
                self.rawstream = rx_streamer.RawIQSamples(self.chB,1,defs.SAMPLE_BLK_SIZE)
                self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_B stream setup ")
                return self.rawstream
                        
            
            else:
                print("iotSDR Device: Channel is not selected correctly")
                return None
        
    def readStream(self,stream):
            
            return  stream.acquireSamples()
            
    
    def closeStream(self,stream):
        
        try:
            del stream.sample_buffer
            stream.stop()
        except AttributeError:
            print("iotSDR Device: stream is not created")