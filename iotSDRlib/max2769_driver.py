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

"""
GPS MAX2769 RF frontend driver
author: embedinn.com
"""    

import max2769_defs
import spidev


class MAX2769(object):

    def __init__(self,SPIchannel=2):
        
        self.SPIchannel = SPIchannel
        self.spi        = spidev.SpiDev()
        
        ## Default MAX settings
        self.spi_init()
        self.gps_0IF_config()
        
    def spi_init(self):
            """
            Initialize the SPI modules.
            :return: nothing
            """
            self.spi.open(self.SPIchannel, 0)
            self.spi.max_speed_hz = 7800000

    def int32_to_int8(self,n):
        mask = (1 << 8) - 1
        return [(n >> k) & mask for k in range(0, 32, 8)]

    def gps_write_spi(self, address, value=None):
            """
            GPS Register Settings
            
            :param address: the reg addr to be written, last 4 bits
            :param value:   the value to be written first, xfer2 needs 
                            bytes list so some convesion logic applied 
            :return: nothing
            """
            reg = (value << 4) & 0xFFFFFFF0
            reg |= (address & 0x0F)
            
            reg_byte_list = self.int32_to_int8(reg)
            reg_byte_list.reverse()

            self.spi.xfer2(reg_byte_list)       
            
     
    def gps_4096IF_config(self):
        addr = 0
        #for reg in max2769_defs.MAX2769_Default_Regs:
        for reg in max2769_defs.MAX2769_Default_AMK_4MS:
    
            regNow = reg 
            self.gps_write_spi(addr,regNow)
            #print(addr,hex(reg))    
            addr += 1
            print("GPS chip is configured for IF=4.0960MHz @ 16.368MSPS")
    
    def gps_0IF_config(self):
        self.gps_write_spi(max2769_defs.MAX2769_CONF1, max2769_defs.CONF1)
        self.gps_write_spi(max2769_defs.MAX2769_CONF2, max2769_defs.CONF2)
        self.gps_write_spi(max2769_defs.MAX2769_CONF3, max2769_defs.CONF3)
        self.gps_write_spi(max2769_defs.MAX2769_PLLCONF, max2769_defs.PLLCONF)
        self.gps_write_spi(max2769_defs.MAX2769_PLLIDR, max2769_defs.PLLIDR)
        self.gps_write_spi(max2769_defs.MAX2769_CFDR, max2769_defs.CFDR)
        print("GPS chip is configured for IF=0MHz @ 4.096MSPS")
