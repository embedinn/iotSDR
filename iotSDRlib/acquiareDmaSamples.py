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

import iotSDR.dma
import numpy as np
import time
from pynq import allocate

import asyncio
import threading

try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        pass
    else:
        def run_loop():
            loop.run_forever()

        asyncio_thread = threading.Thread(target=run_loop)
        asyncio_thread.start()
except:
    print("asyncio loop  Already running")


class rxRawIQSamples():
    def __init__(self, transceiver,blks=1,data_size=1024):
        self.nblks = blks
        self.transceiver  = transceiver

        self.data_size = data_size
        self.running = True
        
        
        """Init DMA Buffers"""
        """TODO:Move this to iotSDR init module"""
        self.dma_txrx = self.transceiver.pl_dma_txrx       

    
    def start(self):
        
        self.transceiver.enable_pl_rx_samples(0)
        self.transceiver.rx_fifo_reset()
        self.transceiver.enable_pl_rx_samples(1)
        self.running = True
        #self.task = asyncio.run_coroutine_threadsafe(self._run_thread(), asyncio.get_event_loop())
    
    def stop(self):
        self.transceiver.enable_pl_rx_samples(0)
        self.transceiver.rx_fifo_reset()
        self.running = False
        self.dma_txrx.recvchannel.stop()
    
               
    def acquireSamples(self,sample_buffer):
            
            # with 4 DMA BDs
            # can be moved to dma trasnfer call
            num_descr = 2
            self.transceiver.set_rx_block_size(sample_buffer.nbytes//num_descr*4)
            
            self.dma_txrx.recvchannel.transfer(sample_buffer)
            self.dma_txrx.recvchannel.wait()

            #return sample_buffer[::2] + 1j * sample_buffer[1::2]

    # Future use
    async def _run_thread(self):
        channel = self.dma_recv.recvchannel
        while self.running:
            channel.transfer(self.input_buffer)
            await channel.wait_async()
            t_data = np.array(self.input_buffer)

            global samples
            samples = t_data[::2] + 1j * t_data[1::2]


class txRawIQSamples():
    def __init__(self, transceiver,cyclic_mode,data_size=1024):
        #self.nblks = blks
        self.transceiver  = transceiver

        self.data_size = data_size
        self.running = True
        
        """Init DMA Buffers"""
        """TODO:Move this to iotSDR init module"""
        self.dma_txrx = self.transceiver.pl_dma_txrx
        self.dma_txrx.sendchannel._cyclic_mode = cyclic_mode
        
    def start(self):
        
        self.running = True
        #self.task = asyncio.run_coroutine_threadsafe(self._run_thread(), asyncio.get_event_loop())
    
    def stop(self):
        self.running = False
        self.dma_txrx.sendchannel.stop()
    
               
    def generateSamples(self,sample_buffer):
            
            # with 4 DMA BDs
            # can be moved to dma trasnfer call
            
            self.dma_txrx.sendchannel.transfer(sample_buffer)
            self.dma_txrx.sendchannel.wait()

            #return sample_buffer[::2] + 1j * sample_buffer[1::2]
    
    # Future Use
    async def _run_thread(self):
        channel = self.dma_recv.recvchannel
        while self.running:
            channel.transfer(self.input_buffer)
            await channel.wait_async()
            t_data = np.array(self.input_buffer)

            global samples
            samples = t_data[::2] + 1j * t_data[1::2]

            
