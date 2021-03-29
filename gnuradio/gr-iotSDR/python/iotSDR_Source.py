#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 gr-iotSDR author.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import sys
sys.path.append("/usr/local/lib/python3.6/dist-packages/iotSDR_Remote/")

import numpy as np
from gnuradio import gr
from iotSDR_Remote import iotSDR_Remote
from iotSDR_defs import *


class iotSDR_Source(gr.sync_block):
	"""
	docstring for block iotSDR_Source
	"""
	def __init__(self, URL,
				Rx_Channel,
				frequency,
				sample_rate,
				bandwidth,
				agc_mode,
				buffer_size):

		gr.sync_block.__init__(self,
			name="iotSDR_Source",
			in_sig=None,
			out_sig=[np.complex64])

		self.url = URL
		self.frequency = frequency
		self.Rx_Channel = Rx_Channel

		self.iotSDR  = iotSDR_Remote.iotSDR_Remote()

		if self.Rx_Channel == 'SubGhz_CH_1':
			self.rx_chan = iotSDR_defs.chan_subGHz_A

		elif self.Rx_Channel == 'SubGhz_CH_2':
			self.rx_chan = iotSDR_defs.chan_subGHz_B

		elif self.Rx_Channel == '2_4Ghz_CH_1':
			self.rx_chan = iotSDR_defs.chan_24GHz_A

		elif self.Rx_Channel == '2_4Ghz_CH_2':
			self.rx_chan = iotSDR_defs.chan_24GHz_B

		self.iotSDR_Init()

		self._frame_count = 0

	def iotSDR_Init(self):

		print("Connecting iotSDR Device: Source : ",self.url)

		if	self.iotSDR.connect(self.url):
			pass
		else:
			exit()


		self.iotSDR.setFrequency(self.rx_chan,self.frequency)

		self.rx_stream = self.iotSDR.setupStream(iotSDR_defs.IOTSDR_RX,self.rx_chan)
		print("iotSDR Initialized",self.rx_stream)


	def iotSDR_Tx(self):
		tone_freq = 30 #Hz
		number_of_samples = 1024

		t    = np.linspace(0, 1, number_of_samples,endpoint=False)
		real = np.cos(2*np.pi*tone_freq*t)
		imag = np.sin(2*np.pi*tone_freq*t)

		tx_samples = real + 1j*imag

		self.iotSDR.setTxLUT(self.tx_chan,tx_samples)

	def iotSDR_Rx(self):
		total_frames = 1
		frames,num_frames = self.iotSDR.readStream(self.rx_stream,total_frames)
		return frames

	def sinosoids(self,N):
		#N = 128

		if self.frequency <= 1000:
			self.frequency +=1
		else:
			self.frequency = 1

		t = np.linspace(0, 1, N,endpoint=False)
		real = (np.cos(2*np.pi*self.frequency*t))
		imag = (np.sin(2*np.pi*self.frequency*t))

		return real + 1j*imag

	def work(self, input_items, output_items):

		self._frame_count +=1

		samples_len = len(output_items[0][:])

		"internal source"
		#samples = self.sinosoids(samples_len)

		"iotSDR Source"
		samples = self.iotSDR_Rx()

		#samples_len = len(samples)
		output_items[0][:] = samples[:samples_len]
		return samples_len