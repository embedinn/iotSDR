from iotSDR_Remote import *
from iotSDR_Remote import iotSDR_defs as defs

iotSDR = iotSDR_Remote()
iotSDR.connect("10.42.0.128:42400")

rx_chan   = defs.chan_subGHz_A
tx_chan   = defs.chan_subGHz_B

freq = 902.2e6
iotSDR.setFrequency(tx_chan,freq)
iotSDR.setFrequency(rx_chan,freq)