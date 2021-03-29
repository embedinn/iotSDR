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


class iotSDR_Sink(gr.sync_block):
	"""
	docstring for block iotSDR_Sink
	"""
	def __init__(self, URL,
			Tx_Channel,
			frequency,
			sample_rate,
			bandwidth,
			rf_gain,
			buffer_size):

		gr.sync_block.__init__(self,
			name="iotSDR_Sink",
			in_sig=[np.complex64],
			out_sig=None)

		self.url = URL
		self.frequency  = frequency
		self.Tx_Channel = Tx_Channel

		if self.Tx_Channel == 'SubGhz_CH_1':
			self.tx_chan = iotSDR_defs.chan_subGHz_A

		elif self.Tx_Channel == 'SubGhz_CH_2':
			self.tx_chan = iotSDR_defs.chan_subGHz_B

		elif self.Tx_Channel == '2_4Ghz_CH_1':
			self.tx_chan = iotSDR_defs.chan_24GHz_A

		elif self.Tx_Channel == '2_4Ghz_CH_2':
			self.tx_chan = iotSDR_defs.chan_24GHz_B

		self.iotSDR  = iotSDR_Remote.iotSDR_Remote()
		self.iotSDR_Init()


	def iotSDR_Init(self):

		print("Connecting iotSDR Device: Sink : ",self.url)

		if	self.iotSDR.connect("10.42.0.128:42400"):
			pass
		else:
			exit()

		freq = 902.2e6

		self.iotSDR.setFrequency(self.tx_chan,freq)

		self.iotSDR_Tx()
		print("iotSDR Transmission started")


	def iotSDR_Tx(self):
		tone_freq = 30 #Hz
		number_of_samples = 1024

		t    = np.linspace(0, 1, number_of_samples,endpoint=False)
		real = np.cos(2*np.pi*tone_freq*t)
		imag = np.sin(2*np.pi*tone_freq*t)

		tx_samples = real + 1j*imag

		self.iotSDR.setTxLUT(self.tx_chan,tx_samples)

	def work(self, input_items, output_items):
		in0 = input_items[0]
		# <+signal processing here+>
		return len(input_items[0])

