
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

import numpy as np
import iotSDR.iotSDR_Device as iotSDR
import iotSDR.iotSDR_defs as defs
import iotSDR.acquiareDmaSamples as trx_streamer


class iotSDR_stream(iotSDR.iotSDR):

    

    def __init__(self,overlay=None,args=0):
        super().__init__(overlay,args)    
        
        
        self.streamA_registry = 0
        self.streamB_registry = 0
        
        
    def setupStream(self,direction,channel):
        
        

        if channel == defs.chan_subGHz_A:
            if self.streamA_registry == 0:
                self.streamA = self.initStream(defs.IOTSDR_RX,defs.chan_subGHz_A)
                self.streamA_registry = 1
                return self.streamA
            else:
                print("iotSDR Device: stream of subGHz channel 1 is already created")
                return self.streamA
                
            
        elif channel == defs.chan_subGHz_B:
            if self.streamB_registry == 0:
                self.streamB = self.initStream(defs.IOTSDR_RX,defs.chan_subGHz_B)
                self.streamB_registry = 1
                return self.streamB
            else:
                print("iotSDR Device: stream of subGHz channel 2 is already created")
                return self.streamB
                
        elif channel == defs.chan_24GHz_A:
            
            if self.streamA_registry == 0:
                self.streamA = self.initStream(defs.IOTSDR_RX,defs.chan_24GHz_A)
                self.streamA_registry = 1
                return self.streamA
            else:
                print("iotSDR Device: stream of 2.4GHz channel 1 is already created")
                return self.streamA
                
        elif channel == defs.chan_24GHz_B:
            if self.streamB_registry == 0:
                self.streamB = self.initStream(defs.IOTSDR_RX,defs.chan_24GHz_B)
                self.streamB_registry = 1
                return self.streamB
            else:
                print("iotSDR Device: stream of 2.4GHz channel 2 is already created")
                return self.streamB
            
    def initStream(self,direction,channel,mode=False):
        self.direction    = direction
        self.channel      = channel
        self._cyclic_mode = mode
        
        if direction == defs.IOTSDR_TX:
            if self.channel == defs.chan_subGHz_A:
                self.chA.tx_samples_select(0)
                self.chA.radio_start_transmission("subGHz")
                
                self.tx_rawstream = trx_streamer.txRawIQSamples(self.chA,self._cyclic_mode,defs.SAMPLE_BLK_SIZE)

                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_A Tx stream setup ")
                return self.tx_rawstream
            
            elif self.channel == defs.chan_subGHz_B:
                self.chB.tx_samples_select(0)
                self.chB.radio_start_transmission("subGHz")
                self.tx_rawstream = trx_streamer.txRawIQSamples(self.chB,self._cyclic_mode,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_B Tx stream setup ")
                return self.tx_rawstream

            elif self.channel == defs.chan_24GHz_A:
                self.chA.tx_samples_select(0)
                self.chA.radio_start_transmission("24GHz")
                
                self.tx_rawstream = trx_streamer.txRawIQSamples(self.chA,self._cyclic_mode,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_A Tx stream setup ")
                return self.tx_rawstream

            elif self.channel == defs.chan_24GHz_B:
                self.chB.rx_samples_select(0)
                self.chB.radio_start_reception("24GHz")

                self.tx_rawstream = trx_streamer.txRawIQSamples(self.chB,self._cyclic_mode,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_B Tx stream setup ")
                return self.tx_rawstream
                
        if direction == defs.IOTSDR_RX:
            if self.channel == defs.chan_subGHz_A:
                self.chA.rx_samples_select(1)
                self.chA.radio_start_reception("subGHz")
                self.rawstream = trx_streamer.rxRawIQSamples(self.chA,1,defs.SAMPLE_BLK_SIZE)

                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_A stream setup ")
                return self.rawstream
            
            elif self.channel == defs.chan_subGHz_B:
                self.chB.rx_samples_select(1)
                self.chB.radio_start_reception("subGHz")
                self.rawstream = trx_streamer.rxRawIQSamples(self.chB,1,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_subGHz_B stream setup ")
                return self.rawstream

            elif self.channel == defs.chan_24GHz_A:
                self.chA.rx_samples_select(2)
                self.chA.radio_start_reception("24GHz")
                
                self.rawstream = trx_streamer.rxRawIQSamples(self.chA,1,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_A stream setup ")
                return self.rawstream

            elif self.channel == defs.chan_24GHz_B:
                self.chB.rx_samples_select(2)
                self.chB.radio_start_reception("24GHz")

                self.rawstream = trx_streamer.rxRawIQSamples(self.chB,1,defs.SAMPLE_BLK_SIZE)
                #self.rawstream.start()
                print("iotSDR Device: Channel: chan_24GHz_B stream setup ")
                return self.rawstream
                        
            
            else:
                print("iotSDR Device: Channel is not selected correctly")
                return None
    
    def activateStream(self,stream):        
        try:
            stream.start()
        except AttributeError:
            print("iotSDR Device: stream is already running")
            
    def deactivateStream(self,stream):      
        try:
            stream.stop()
            del stream
        except AttributeError:
            print("iotSDR Device: stream is not created")    
    
    def readStreamFrames(self,channel,num_blks=1):
            if channel == defs.chan_subGHz_A:
                stream =  self.streamA
            elif channel == defs.chan_subGHz_B:
                stream =  self.streamB
                
                
            blk_count = 0
            blk_drop  = 0
            
            blks = np.array([])
            self.rawstream.transceiver.rx_fifo_reset()
            self.rawstream.transceiver.enable_pl_rx_samples(1)
            for _ in range(num_blks+0):
                    
                blk  = stream.acquireSamples()
                blks = np.concatenate((blks,blk))
                blk_count +=1
            
            return blks[blk_drop*defs.SAMPLE_BLK_SIZE:],blk_count-1  
 
    
    def readStream(self,stream,samples_buffer):
                
            stream.acquireSamples(samples_buffer)
            
        
    def readStream_remote(self,stream):
            if stream == defs.chan_subGHz_A:
                return  self.streamA.acquireSamples()
            elif stream == defs.chan_subGHz_B:
                return  self.streamB.acquireSamples()
    

    def writeStream(self,stream,samples_buffer):
                
            stream.generateSamples(samples_buffer)
