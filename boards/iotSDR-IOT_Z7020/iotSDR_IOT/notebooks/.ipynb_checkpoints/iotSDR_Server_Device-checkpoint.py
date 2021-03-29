
from concurrent import futures
import logging

import grpc

import iotSDR_pb2
import iotSDR_pb2_grpc

import numpy as np

from pynq import Overlay
import iotSDR_Device as iotSDR
import iotSDR_streaming as iotSDR_stream

class ConfigSDR(iotSDR_pb2_grpc.ConfigSDRServicer):
    
    def __init__(self):
        
        self.initDevice()
        self.streamID = 0

    """
    Initialize bitfile
    """
    def initDevice(self):
        
        self.overlay = Overlay('/home/xilinx/pynq/overlays/base/dualRxTxDmaOTAv1.3.1.bit', download=True)
        print("iotSDR Confg: Bitfile Loaded")
        args  = 0
        #self.device = iotSDR.iotSDR(self.overlay,args)
        self.device = iotSDR_stream.iotSDR_stream(self.overlay,0)
        print("iotSDR Confg: Device Initialized")

    """
    Frequency settings API
    """
    def setFrequency(self, request, context):
        print("iotSDR Confg: Frequency set request: Chan:",request.freq,request.chan)
        
        status = self.device.setFrequency(request.chan,request.freq)
        return iotSDR_pb2.status(status=status)
    
    def getFrequency(self,request,context):
        print("iotSDR Confg: Frequency get request: chan:",request.chan)
        freq = self.device.getFrequency(request.chan)
        print(freq)
        return iotSDR_pb2.Rf_freq(freq=freq)

    def listFrequencies(self,request,context):
        freqBands = {1:(389.5e6,510e6),
                     2:(779e6,1020e6)
                     }

        print("iotSDR Confg: Range of frequencies {} of channel {}:".format(freqBands,request.chan))

        for key in freqBands:
            freq_pair = iotSDR_pb2.freqPair(band=key,min_freq=freqBands[key][0],max_freq=freqBands[key][1])
            yield (iotSDR_pb2.ListFreq(ranges=freq_pair))

    """
    Sampling Rate settings API
    """

    def setSampleRate(self,request,context):
        print("iotSDR Confg: Setsampling rate request:",request.chan,request.rate)
        
        self.device.setSampleRate(0,request.chan,request.rate)
        return iotSDR_pb2.status(status=int(request.rate))

    def getSampleRate(self,request,context):
        SamplingRate = 2e6
        print("iotSDR Confg: Getsampling rate request:",request.chan)
        
        set_rate = self.device.getSampleRate(0,request.chan)
        
        return iotSDR_pb2.status(status= set_rate)

    def listSampleRates(self,request,context):
        rates = [4e6,
                    2e6,
                    round((4000/3)*1e3,2),
                    1e6,800e3,
                    round((2000/3)*1e3,2),
                    500e3,
                    400e3]

        for rate in rates:
            yield iotSDR_pb2.sampling_rates(rate=rate)

        print("iotSDR Confg: supported sample Rates:",rates)


    """
    Set Tx Gain APIs
    """
    def setGain(self,request,context):
        
        print("iotSDR Confg: St Gain request:",request.chan,request.gain)
        gain = self.device.setGain(request.chan,request.gain)
        return iotSDR_pb2.status(status=gain)

    def getGain(self,request,context):
        print("iotSDR Confg: Get Gain request:",request.chan)
        gain = self.device.getGain(request.chan)
        return iotSDR_pb2.status(status=gain)

    def getGainRange(self,request,context):
        print("iotSDR Confg: Range of Gain request:",request.chan)
        rang = self.device.getGainRange(request.chan)
        return iotSDR_pb2.gainRange(min=rang[0],max=rang[1])


    def setTxLUT(self,request,context):
        print("iotSDR Confg: Tx LUT Buffer Set request of channel:",request.chan)
        real = np.frombuffer(request.samples_real, dtype=np.int16)
        imag = np.frombuffer(request.samples_imag, dtype=np.int16)
        #print(("Server:",real))
        IQsamples = real+1j*imag
        
        self.device.setTxLUT(request.chan,IQsamples)
        print("iotSDR Confg: Continious Tx Start")
        return iotSDR_pb2.status(status=1)

class stramingIQ(iotSDR_pb2_grpc.ConfigSDRServicer):

    def __init__(self,config_sdr):

        self.streamID = 0
        self.device   = config_sdr.device
        

    """Streaming IQ Samples"""
    def chirp(self):
        f = 12 #Hz
        N = 1024

        t = np.linspace(0, 1, N,endpoint=False)
        for f in range(0,1):
            real = (np.cos(2*np.pi*f*t))*(2**15 - 1)
            imag = (np.sin(2*np.pi*f*t))*(2**15 - 1)

            real = real.astype(np.int16)
            imag = imag.astype(np.int16)
            yield real

    def setupStream(self,request,context):

        self.stream_handle = self.device.setupStream(request.direction,request.chan)
        self.streamID +=1
        return iotSDR_pb2.streamID(id=self.streamID)
        print("iotSDR Stream: Stream configured:",self.streamID)

    def sendIQsampleStream(self,request,context):
        """
        f = 12 #Hz
        N = 4*1024

        t = np.linspace(0, 1, N,endpoint=False)
        real = (np.cos(2*np.pi*f*t))*(2**15 - 1)
        imag = (np.sin(2*np.pi*f*t))*(2**15 - 1)

        real = real.astype(np.int16)
        imag = imag.astype(np.int16)
        print(real)
        """
        print("iotSDR Stream: Sending Frames")

        for frames in range(0,request.numOfFrames):
            iqSampleBlk = self.device.readStream(self.stream_handle)
            #print(iqSampleBlk)
            yield iotSDR_pb2.iqSampleFrames(frame = iqSampleBlk.real.tobytes())
        

        print("iotSDR Stream: Raw IQ samples sent:",frames)



        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print("")
    print("############################################################################")
    print( " _         _    ____   ____   ____    ____                                 ")
    print( "(_)  ___  | |_ / ___| |  _ \ |  _ \  / ___|   ___  _ __ __   __  ___  _ __ ")
    print( "| | / _ \ | __|\___ \ | | | || |_) | \___ \  / _ \| '__|\ \ / / / _ \| '__|")
    print( "| || (_) || |_  ___) || |_| ||  _ <   ___) ||  __/| |    \ V / |  __/| |   ")
    print( "|_| \___/  \__||____/ |____/ |_| \_\ |____/  \___||_|     \_/   \___||_|   ")
    print("############################################################################")
    print("")

    config_sdr = ConfigSDR()

    iotSDR_pb2_grpc.add_ConfigSDRServicer_to_server(config_sdr, server)
    iotSDR_pb2_grpc.add_streamingIQserviceServicer_to_server(stramingIQ(config_sdr), server)
    server.add_insecure_port('[::]:42400')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    
    
    logging.basicConfig()
    serve()