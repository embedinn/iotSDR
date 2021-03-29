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

Register definations  for MAx2769 GPS Chip
author: embedinn.com
"""

# Address Registers

""" Name                address     default value """
MAX2769_CONF1           = 0x0       # 0xA2919A3
MAX2769_CONF2           = 0x1       # 0x0550288
MAX2769_CONF3           = 0x2       # 0xEAFF1DC
MAX2769_PLLCONF         = 0x3       # 0x9EC0008
MAX2769_PLLIDR          = 0x4       # 0x0C00080
MAX2769_FDIV            = 0x5       # 0x8000070
MAX2769_STRM            = 0x6       # 0x8000000
MAX2769_CFDR            = 0x7       # 0x10061B2
MAX2769_TEST1           = 0x8       # 0x1E0F401
MAX2769_TEST2           = 0x9       # 0x14C0402


""" MAX2769 Registers default values """

	             
MAX2769_Default_Regs = [
    #default value               address
    0xA2919A3,               # MAX2769_CONF1         
    0x0550288,               # MAX2769_CONF2  
    0xEAFF1DC,               # MAX2769_CONF3  
    0x9EC0008,               # MAX2769_PLLCONF
    0x0C00080,               # MAX2769_PLLIDR 
    0x8000070,               # MAX2769_FDIV   
    0x8000000,               # MAX2769_STRM   
    0x10061B2,               # MAX2769_CFDR   
    0x1E0F401,               # MAX2769_TEST1  
    0x14C0402                # MAX2769_TEST2  
]

MAX2769_Default_AMK = [
    0xBFF1AA3,               # MAX2769_CONF1
    0x8550288,               # MAX2769_CONF2
    0xEAFF000,               # MAX2769_CONF3
    0x9EC0208,               # MAX2769_PLLCONF
    0x0C00080,               # MAX2769_PLLIDR 
    0x8000070,               # MAX2769_FDIV
    0x8000000,               # MAX2769_STRM  
    0x001FFF2,               # MAX2769_CFDR
    0x1E0F401,               # MAX2769_TEST1  
    0x14C0402                # MAX2769_TEST2 
]


MAX2769_Default_AMK_4MS = [
    0xBFF1FE3,               # MAX2769_CONF1
    0x8550288,               # MAX2769_CONF2
    0xEAFF000,               # MAX2769_CONF3
    0x9AC0208,               # MAX2769_PLLCONF
    0xC080800,               # MAX2769_PLLIDR 
    0x8000070,               # MAX2769_FDIV
    0x8000000,               # MAX2769_STRM  
    0x001FFF2,               # MAX2769_CFDR
    0x1E0F401,               # MAX2769_TEST1  
    0x14C0402                # MAX2769_TEST2 
]


"""
 *Ref: MAX2769 Table 6
 *MAX2769 Register bit positions
"""

""" Name                     bit     Description"""
MAX2769_CONF1_CHIPEN       =   27    # Chip enable  
MAX2769_CONF1_IDLE         =   26    # Idle enable  
MAX2769_CONF1_ILNA1        =   22    # LNA1 current  
MAX2769_CONF1_ILNA2        =   20    # LNA2 current  
MAX2769_CONF1_ILO          =   18    # LO buffer current  
MAX2769_CONF1_IMIX         =   16    # Mixer Current  
MAX2769_CONF1_MIXPOLE      =   15    # Mixer Pole selection  
MAX2769_CONF1_LNAMODE      =   13    # LNA Mode Select  
MAX2769_CONF1_MIXEN        =   12    # Mixer enable  
MAX2769_CONF1_ANTEN        =   11    # Antenna Bias Enable  
MAX2769_CONF1_FCEN         =   5     # IF Center Frequency  
MAX2769_CONF1_FBW          =   3     # IF Filter Center Bandwidth  
MAX2769_CONF1_F3OR5        =   2     # Filter Order Select  
MAX2769_CONF1_FCENX        =   1     # Polyphase filter Select  
MAX2769_CONF1_FGAIN        =   0     # IF Filter Gain Select  
    
"""CONF2 """      
MAX2769_CONF2_IQEN         =   27    # I and Q Channels Enable  
MAX2769_CONF2_GAINREF      =   15    # AGC Gain  
MAX2769_CONF2_AGCMODE      =   11    # AGC Mode  
MAX2769_CONF2_FORMAT       =   9     # Output Data Format  
MAX2769_CONF2_BITS         =   6     # Num of bits in ADC  
MAX2769_CONF2_DRVCFG       =   4     # Output Driver Configuration  
MAX2769_CONF2_LOEN         =   3     # LO buffer enable  
MAX2769_CONF2_DIEID        =   0     # Identify version of IC  

""" CONF3 """
MAX2769_CONF3_GAININ       =   22  # PGA Gain  
MAX2769_CONF3_FSLOWEN      =   21  # Low value of ADC full-scale... 
MAX2769_CONF3_HILOADEN     =   20  # Output driver strength HI-load 
MAX2769_CONF3_ADCEN        =   19  # ADC Enable  
MAX2769_CONF3_DRVEN        =   18  # Output Driver Enable  
MAX2769_CONF3_FOFSTEN      =   17  # Filter DC... 
MAX2769_CONF3_FILTEN       =   16  # IF Filter Enable  
MAX2769_CONF3_FHIPEN       =   15  # Highpass Coupling Enable  
MAX2769_CONF3_PGAIEN       =   13  # I-channel PGA Enable  
MAX2769_CONF3_PGAQEN       =   12  # Q-channel PGA Enable  
MAX2769_CONF3_STRMEN       =   11  # DSP interface...  
MAX2769_CONF3_STRMSTART    =   10  # ...  
MAX2769_CONF3_STRMSTOP     =   9   # ...  
MAX2769_CONF3_STRMCOUNT    =   6   # ...  
MAX2769_CONF3_STRMBITS     =   4   # ...  
MAX2769_CONF3_STAMPEN      =   3   # ...  
MAX2769_CONF3_TIMESYNCEN   =   2   # ...  
MAX2769_CONF3_DATSYNCEN    =   1   # ...  
MAX2769_CONF3_STRMRST      =   0   # ...  

""" PLL """
MAX2769_PLL_VCOEN          =  27   # VCO Enable  
MAX2769_PLL_IVCO           =  26   # VCO Current Select  
MAX2769_PLL_REFOUTEN       =  24   # Clock buffer enable  
MAX2769_PLL_REFDIV         =  21   # Clock Output Divider Ratio  
MAX2769_PLL_IXTAL          =  19   # Current for XTAL  
MAX2769_PLL_XTALCAP        =  14   # Digital Load Cap for XTAL  
MAX2769_PLL_LDMUX          =  10   # LD pin output select  
MAX2769_PLL_ICP            =  9    # Charge Pump current  
MAX2769_PLL_PFDEN          =  8    # ...   
MAX2769_PLL_CPTEST         =  4    # Charge Pump Test   
MAX2769_PLL_INT_PLL        =  3    # PLL Mode Ctl  
MAX2769_PLL_PWRSAV         =  2    # PLL Power Save  

""" PLL Integer Division Ratio """
MAX2769_PLLIDR_NDIV        =  13   # PLL Integer Division Ratio  
MAX2769_PLLIDR_RDIV        =  3    # PLL Reference Division Ratio  

""" PLL Integer Division Ratio """
MAX2769_PLLDR_FDIV         =  8    # PLL Fractional Divider Ratio  

""" DSP Interface """
MAX2769_DSP_FRAMECOUNT     =  27  

""" Clock Fractional Division Ratio """
MAX2769_CFDR_L_CNT         =  16   # L Counter Value  
MAX2769_CFDR_M_CNT         =  4    # M Counter Value  
MAX2769_CFDR_FCLKIN        =  3    # Frac. Clock Divider  
MAX2769_CFDR_ADCCLK        =  2    # ADC Clock Selection  
MAX2769_CFDR_SERCLK        =  1    # Serializer Clock Selection  
MAX2769_CFDR_MODE          =  0    # DSP Interface Mode Selection


MAX2769_CONF3_RESERVED   = (1 << 14)
MAX2769_PLLCONF_RESERVED = (1 << 23)
MAX2769_FDIV_RESERVED  = 0b01110000


CONF1 = \
	(0b1            << MAX2769_CONF1_CHIPEN ) |  \
	(0b0            << MAX2769_CONF1_IDLE   ) |  \
	(0b1111         << MAX2769_CONF1_ILNA1  ) |  \
	(0b11           << MAX2769_CONF1_ILNA2  ) |  \
	(0b11           << MAX2769_CONF1_ILO    ) |  \
	(0b11           << MAX2769_CONF1_IMIX   ) |  \
	(0b0            << MAX2769_CONF1_MIXPOLE) |  \
	(0b01           << MAX2769_CONF1_LNAMODE) |  \
	(0b1            << MAX2769_CONF1_MIXEN  ) |  \
	(0b0            << MAX2769_CONF1_ANTEN  ) |  \
	(0b111111       << MAX2769_CONF1_FCEN   ) |  \
	(0b00           << MAX2769_CONF1_FBW    ) |  \
	(0b0            << MAX2769_CONF1_F3OR5  ) |  \
	(0b0            << MAX2769_CONF1_FCENX  ) |  \
	(0b1            << MAX2769_CONF1_FGAIN  )

CONF2 = \
	(0b1            << MAX2769_CONF2_IQEN   ) |  \
	(0b10101010     << MAX2769_CONF2_GAINREF) |  \
	(0b01           << MAX2769_CONF2_AGCMODE) |  \
	(0b01           << MAX2769_CONF2_FORMAT ) |  \
	(0b010          << MAX2769_CONF2_BITS   ) |  \
	(0b00           << MAX2769_CONF2_DRVCFG ) |  \
	(0b1            << MAX2769_CONF2_LOEN   ) |  \
	(0b00           << MAX2769_CONF2_DIEID  )

CONF3 = \
	MAX2769_CONF3_RESERVED | \
	(0b111010       << MAX2769_CONF3_GAININ    ) |  \
	(0b1            << MAX2769_CONF3_FSLOWEN   ) |  \
	(0b0            << MAX2769_CONF3_HILOADEN  ) |  \
	(0b1            << MAX2769_CONF3_ADCEN     ) |  \
	(0b1            << MAX2769_CONF3_DRVEN     ) |  \
	(0b1            << MAX2769_CONF3_FOFSTEN   ) |  \
	(0b1            << MAX2769_CONF3_FILTEN    ) |  \
	(0b0            << MAX2769_CONF3_FHIPEN    ) |  \
	(0b1            << MAX2769_CONF3_PGAIEN    ) |  \
	(0b1            << MAX2769_CONF3_PGAQEN    ) |  \
	(0b0            << MAX2769_CONF3_STRMEN    ) |  \
	(0b0            << MAX2769_CONF3_STRMSTART ) |  \
	(0b0            << MAX2769_CONF3_STRMSTOP  ) |  \
	(0b111          << MAX2769_CONF3_STRMCOUNT ) |  \
	(0b11           << MAX2769_CONF3_STRMBITS  ) |  \
	(0b0            << MAX2769_CONF3_STAMPEN   ) |  \
	(0b0            << MAX2769_CONF3_TIMESYNCEN) |  \
	(0b0            << MAX2769_CONF3_DATSYNCEN ) |  \
	(0b0            << MAX2769_CONF3_STRMRST   )

PLLCONF = \
	MAX2769_PLLCONF_RESERVED | \
	(0b1          << MAX2769_PLL_VCOEN   ) |    \
	(0b0          << MAX2769_PLL_IVCO    ) |    \
	(0b1          << MAX2769_PLL_REFOUTEN) |    \
	(0b01         << MAX2769_PLL_REFDIV  ) |    \
	(0b01         << MAX2769_PLL_IXTAL   ) |    \
	(0b10000      << MAX2769_PLL_XTALCAP ) |    \
	(0b0000       << MAX2769_PLL_LDMUX   ) |    \
	(0b1          << MAX2769_PLL_ICP     ) |    \
	(0b0          << MAX2769_PLL_PFDEN   ) |    \
	(0b000        << MAX2769_PLL_CPTEST  ) |    \
	(0b1          << MAX2769_PLL_INT_PLL ) |    \
	(0b0          << MAX2769_PLL_PWRSAV  )

PLLIDR = \
	(1540         << MAX2769_PLLIDR_NDIV) | \
	(16           << MAX2769_PLLIDR_RDIV)

CFDR = \
	(1024         << MAX2769_CFDR_L_CNT ) | \
	(1024         << MAX2769_CFDR_M_CNT ) | \
	(0            << MAX2769_CFDR_FCLKIN) | \
	(0            << MAX2769_CFDR_ADCCLK) | \
	(1            << MAX2769_CFDR_SERCLK) | \
	(0            << MAX2769_CFDR_MODE  )