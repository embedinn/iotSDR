"""iotSDR gRPC client """

from __future__ import print_function
import logging
import numpy as np
import grpc

#from .iotSDR_pb2 import *
#from .iotSDR_pb2_grpc import *

import iotSDR_pb2
import iotSDR_pb2_grpc


class iotSDR_Remote():
    def __init__(self):
        self.TIMEOUT_SEC = 3

    def connect(self,URL='localhost:50051'):
        self.url = URL
        channel = grpc.insecure_channel(self.url)

        if self.grpc_server_on(channel):
            print("Connected with iotSDR Remote Server",self.url)
        else:
            print("Unable to connect with iotSDR Server",self.url)
            return False

        self.stub = iotSDR_pb2_grpc.ConfigSDRStub(channel)
        self.stub_stream = iotSDR_pb2_grpc.streamingIQserviceStub(channel)

        return True

    def grpc_server_on(self,channel):# -> bool:
        try:
            grpc.channel_ready_future(channel).result(timeout=self.TIMEOUT_SEC)
            return True
        except grpc.FutureTimeoutError:
            return False

        self.stub = iotSDR_pb2_grpc.ConfigSDRStub(channel)
        self.stub_stream = iotSDR_pb2_grpc.streamingIQserviceStub(channel)
        #return self.stub

    def setFrequency(self,chan,freq):
        response = self.stub.setFrequency(iotSDR_pb2.RFfreq_config(chan=chan,freq=freq))
        #print("iotSDR Frequency updated: ",response.freq)
        return  response.freq

    def getFrequency(self,chan):
        response = self.stub.getFrequency(iotSDR_pb2.Rf_chan(chan=chan))
        print("iotSDR Tuned at Frequency: ",response.freq)

    def listFrequencies(self,chan):
        freqList = []
        for response in self.stub.listFrequencies(iotSDR_pb2.Rf_chan(chan=chan)):
            freqList.append(response)

        print("iotSDR Frequency list: ", freqList)
        return freqList

    # Sampling Rate APIs

    def setSampleRate(self,direction,chan,rate):
        response = self.stub.setSampleRate(iotSDR_pb2.SamplingRate_config(direction=direction,chan=chan,rate=rate))
        print("iotSDR Sampling Rate updated: ",response.status)
        return response.status

    def getSampleRate(self,chan):
        response = self.stub.getSampleRate(iotSDR_pb2.Rf_chan(chan=chan))
        print("iotSDR Sampling rate get response: ",response.status)
        return response.status

    def listSampleRates(self,chan):
        rates = []
        for response in self.stub.listSampleRates(iotSDR_pb2.Rf_chan(chan=chan)):
            rates.append(response.rate)

        print("iotSDR Supported Rates:",rates)
        return rates

    # Tx Gain APIs

    def setGain(self,chan,gain):
        response = self.stub.setGain(iotSDR_pb2.tx_gain(chan=chan,gain=gain))
        print("iotSDR Transmitter Gain set")
        return response.status

    def getGain(self,chan):
        response = self.stub.getGain(iotSDR_pb2.Rf_chan(chan=0))
        print("iotSDR Transmitter Gain get",response.status)
        return response.status

    def getGainRange(self,chan):
        response = self.stub.getGainRange(iotSDR_pb2.Rf_chan(chan=0))
        print("iotSDR Transmitter Gain Range:",response.min,response.max)
        return (response.min,response.max)

    # Set Transmitter LUT Buffer
    def setTxLUT(self,chan,IQsamples):

        real = IQsamples.real*(2**13 - 1)
        imag = IQsamples.imag*(2**13 - 1)

        real = real.astype(np.int16)
        imag = imag.astype(np.int16)
        #print(real)
        response = self.stub.setTxLUT(iotSDR_pb2.txLUT(chan=chan,samples_real=real.tobytes(),
                                                        samples_imag=imag.tobytes()))

        #print("iotSDR Transmitter LUT Buffer set:",response.status)
        #return response.status

    def setupStream(self,direction,chan):
        response = self.stub_stream.setupStream(iotSDR_pb2.streamSetupRequest(direction=direction,chan=chan))
        return response.id

    # Streeaming APIs
    def generatorStream(self,chan,numOfFrames):

        self.count = 0
        #yield self.stub_stream.sendIQsampleStream(iotSDR_pb2.status(status=1))
        for response in self.stub_stream.sendIQsampleStream(iotSDR_pb2.framesRequest(numOfFrames=numOfFrames)):
            self.count +=1
            yield response

    def readStream(self,chan,numOfFrames):

        frame_count = 0
        frames_real = np.array([],dtype=np.int16)
        frames_imag = np.array([],dtype=np.int16)
        
        for frame in (self.generatorStream(chan,numOfFrames+1)):
            
            frame_real = np.frombuffer(frame.frame_real)
            frame_imag = np.frombuffer(frame.frame_imag)

            frames_real = np.concatenate((frames_real,frame_real))
            frames_imag = np.concatenate((frames_imag,frame_imag))

            #print(frame,len(frame))
            frame_count +=1
            
        
        frames_complex = frames_real + 1j*frames_imag
        
        return frames_complex[4096:], frame_count
