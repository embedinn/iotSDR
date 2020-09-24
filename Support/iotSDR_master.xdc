## This file is a general .xdc for the iotSDR Rev. A
## It is compatible with the iotSDR iot_Z10 and iot_Z20
## To use it in a project:
## - uncomment the lines corresponding to used pins
## - rename the used ports (in each line, after get_ports) according to the top level signal names in the project


##4-LEDs 
#set_property -dict { PACKAGE_PIN N15   IOSTANDARD LVCMOS25 } [get_ports { LED_1 }]; #IO_L21P_T3_DQS_AD14P_35
#set_property -dict { PACKAGE_PIN N16   IOSTANDARD LVCMOS25 } [get_ports { LED_2 }]; #IO_L21N_T3_DQS_AD14N_35
#set_property -dict { PACKAGE_PIN L14   IOSTANDARD LVCMOS25 } [get_ports { LED_3 }]; #IO_L22P_T3_AD7P_35
#set_property -dict { PACKAGE_PIN L15   IOSTANDARD LVCMOS25 } [get_ports { LED_4 }]; #IO_L22N_T3_AD7N_35




##Pmod Header J1
#set_property -dict { PACKAGE_PIN E17   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[0] }]; #IO_L3P_T0_DQS_AD1P_35	   
#set_property -dict { PACKAGE_PIN D18   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[1] }]; #IO_L3N_T0_DQS_AD1N_35           
#set_property -dict { PACKAGE_PIN C20   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[2] }]; #IO_L1P_T0_AD0P_35           
#set_property -dict { PACKAGE_PIN B20   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[3] }]; #IO_L1N_T0_AD0N_35            
#set_property -dict { PACKAGE_PIN F19   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[4] }]; #IO_L15P_T2_DQS_AD12P_35      
#set_property -dict { PACKAGE_PIN F20   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[5] }]; #IO_L15N_T2_DQS_AD12N_35            
#set_property -dict { PACKAGE_PIN L19   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[6] }]; #IO_L9P_T1_DQS_AD3P_35          
#set_property -dict { PACKAGE_PIN L20   IOSTANDARD LVCMOS25 } [get_ports { PMOD35[7] }]; #IO_L9N_T1_DQS_AD3N_35 

##Pmod Header J2
#set_property -dict { PACKAGE_PIN V17   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[0] }]; #IO_L21P_T3_DQS_34   
#set_property -dict { PACKAGE_PIN V18   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[1] }]; #IO_L21N_T3_DQS_34             
#set_property -dict { PACKAGE_PIN W18   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[2] }]; #IO_L22P_T3_34            
#set_property -dict { PACKAGE_PIN N20   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[3] }]; #IO_L14P_T2_SRCC_34            
#set_property -dict { PACKAGE_PIN P20   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[4] }]; #IO_L14N_T2_SRCC_34      
#set_property -dict { PACKAGE_PIN V15   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[5] }]; #IO_L10P_T1_34           
#set_property -dict { PACKAGE_PIN T10   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[6] }]; #IO_L1N_T0_34        
#set_property -dict { PACKAGE_PIN T12   IOSTANDARD LVCMOS33 } [get_ports { PMOD34[7] }]; #IO_L2P_T0_34  


##RF_CH_2 Differential Signals
#set_property -dict { PACKAGE_PIN L16  [get_ports clk2_in_p_0]       #  clock_in        #IO_L11P_T1_SRCC_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports clk2_in_p_0]
#set_property -dict IOSTANDARD LVDS_25 [get_ports clk2_in_n_0]

#set_property -dict PACKAGE_PIN E18    [get_ports {rxd2_p_09[0]}]    # lvds 09 reciever #IO_L5P_T0_AD9P_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd2_n_09[0]}]
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd2_p_09[0]}]

#set_property -dict PACKAGE_PIN B19    [get_ports {rxd2_p_24[0]}]    # lvds 24 reciever #IO_L2P_T0_AD8P_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd2_n_24[0]}]
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd2_p_24[0]}]

#set_property -dict { PACKAGE_PIN D19  [get_ports  txd2_p_0[0]]      # transmitter      #IO_L4P_T0_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports  txd2_p_0[0]]
#set_property -dict IOSTANDARD LVDS_25 [get_ports  txd2_n_0[0]]

#set_property -dict { PACKAGE_PIN H16  [get_ports tx2_out_p_0]       #clock_out         #IO_L13P_T2_MRCC_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports tx2_out_p_0]
#set_property -dict IOSTANDARD LVDS_25 [get_ports tx2_out_n_0]


##RF_CH_1 Differential Signals

#set_property -dict { PACKAGE_PIN J18 [get_ports  clk1_in_p_0]       #  clock_in        # IO_L14P_T2_AD4P_SRCC_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports clk1_in_p_0]
#set_property -dict IOSTANDARD LVDS_25 [get_ports clk1_in_n_0]

#set_property -dict PACKAGE_PIN G19    [get_ports {rxd1_p_09[0]}]    # lvds 09 reciever # IO_L18P_T2_AD13P_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd1_n_09[0]}]
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd1_p_09[0]}]

#set_property -dict PACKAGE_PIN G17    [get_ports {rxd1_p_24[0]}]    # lvds 24 reciever # IO_L16P_T2_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd1_n_24[0]}]
#set_property -dict IOSTANDARD LVDS_25 [get_ports {rxd1_p_24[0]}]

#set_property -dict { PACKAGE_PIN J20  [get_ports  txd1_p_0[0]]      # transmitter      # IO_L17P_T2_AD5P_35 
#set_property -dict IOSTANDARD LVDS_25 [get_ports  txd1_p_0[0]]
#set_property -dict IOSTANDARD LVDS_25 [get_ports  txd1_n_0[0]]

#set_property -dict { PACKAGE_PIN K17  [get_ports tx1_out_p_0]       #clock_out         # IO_L12P_T1_MRCC_35
#set_property -dict IOSTANDARD LVDS_25 [get_ports tx1_out_p_0]
#set_property -dict IOSTANDARD LVDS_25 [get_ports tx1_out_n_0]



###RF_CH_2 Single_Ended_Signals
 ##SPI_Signals Ch2
 
#set_property -dict { PACKAGE_PIN V12  IOSTANDARD LVCMOS33 } [get_ports { MOSI2 }]; #IO_L4P_T0_34
#set_property -dict { PACKAGE_PIN V13  IOSTANDARD LVCMOS33 } [get_ports { MISO2 }]; #IO_L3N_T0_DQS_34
#set_property -dict { PACKAGE_PIN T15  IOSTANDARD LVCMOS33 } [get_ports { SELN2 }]; #IO_L5N_T0_34
#set_property -dict { PACKAGE_PIN U14  IOSTANDARD LVCMOS33 } [get_ports { SCLK2 }]; #IO_L11P_T1_SRCC_34
 
 ##Control_Signals Ch2
#set_property -dict { PACKAGE_PIN R14  IOSTANDARD LVCMOS33 } [get_ports { IRQ2 }];    #IO_L6N_T0_VREF_34
#set_property -dict { PACKAGE_PIN U19  IOSTANDARD LVCMOS33 } [get_ports { CLK_0_2 }]; #IO_L12N_T1_MRCC_34
#set_property -dict { PACKAGE_PIN P14  IOSTANDARD LVCMOS33 } [get_ports { RST_EN_2}]; #IO_L6P_T0_34




###RF_CH_1 Single_Ended_Signals
 ##SPI_Signals Ch1
 
#set_property -dict { PACKAGE_PIN U12  IOSTANDARD LVCMOS33 } [get_ports { MOSI1 }]; #IO_L2N_T0_34
#set_property -dict { PACKAGE_PIN U13  IOSTANDARD LVCMOS33 } [get_ports { MISO1 }]; #IO_L3P_T0_DQS_PUDC_B_34
#set_property -dict { PACKAGE_PIN Y14  IOSTANDARD LVCMOS33 } [get_ports { SELN1 }]; #IO_L8N_T1_34
#set_property -dict { PACKAGE_PIN U15  IOSTANDARD LVCMOS33 } [get_ports { SCL1 }];  #IO_L11N_T1_SRCC_34
 
 ##Control_Signals Ch1
#set_property -dict { PACKAGE_PIN Y17  IOSTANDARD LVCMOS33 } [get_ports { IRQ1 }];    #IO_L7N_T1_34
#set_property -dict { PACKAGE_PIN U18  IOSTANDARD LVCMOS33 } [get_ports { CLK_0_1 }]; #IO_L12P_T1_MRCC_34
#set_property -dict { PACKAGE_PIN W14  IOSTANDARD LVCMOS33 } [get_ports { RST_EN_1}]; #IO_L8P_T1_34 


##EEPROM I2C
#set_property -dict { PACKAGE_PIN R19  IOSTANDARD LVCMOS33 } [get_ports { AT24_SCL }]; #IO_0_34
#set_property -dict { PACKAGE_PIN T11  IOSTANDARD LVCMOS33 } [get_ports { AT24_SDA }]; #IO_L1P_T0_34 



##LEDs --3.3V
#set_property -dict { PACKAGE_PIN T16   IOSTANDARD LVCMOS33 } [get_ports { LED_TXRX_1 }]; #IO_L9P_T1_DQS_34
#set_property -dict { PACKAGE_PIN Y16   IOSTANDARD LVCMOS33 } [get_ports { LED_TXRX_2 }]; #IO_L17N_T2_34



##GNSS CHIP


#set_property -dict { PACKAGE_PIN N18   IOSTANDARD LVCMOS33 } [get_ports { G_SCLK }];    #IO_L13P_T2_MRCC_34
#set_property -dict { PACKAGE_PIN P19    IOSTANDARD LVCMOS33 } [get_ports { G_CLKOUT }]; #IO_L13N_T2_MRCC_34
#set_property -dict { PACKAGE_PIN W20   IOSTANDARD LVCMOS33 } [get_ports { G_IDLE }];    #IO_L16N_T2_34
#set_property -dict { PACKAGE_PIN Y18   IOSTANDARD LVCMOS33 } [get_ports { G_SHDN }];    #IO_L17P_T2_34
#set_property -dict { PACKAGE_PIN Y19    IOSTANDARD LVCMOS33 } [get_ports { G_SDATA }];  #IO_L17N_T2_34
#set_property -dict { PACKAGE_PIN V16   IOSTANDARD LVCMOS33 } [get_ports { G_PGM }];     #IO_L18P_T2_34
#set_property -dict { PACKAGE_PIN W16   IOSTANDARD LVCMOS33 } [get_ports { G_CS }];      #IO_L18N_T2_34
#set_property -dict { PACKAGE_PIN R16    IOSTANDARD LVCMOS33 } [get_ports { G_10 }];     #IO_L19P_T3_34
#set_property -dict { PACKAGE_PIN R17   IOSTANDARD LVCMOS33 } [get_ports { G_I1 }];      #IO_L19N_T3_VREF_34
#set_property -dict { PACKAGE_PIN T17   IOSTANDARD LVCMOS33 } [get_ports { G_Q0 }];      #IO_L20P_T3_34
#set_property -dict { PACKAGE_PIN P15   IOSTANDARD LVCMOS33 } [get_ports { G_Q1 }];      #IO_L24P_T3_34
#set_property -dict { PACKAGE_PIN P16   IOSTANDARD LVCMOS33 } [get_ports { G_ANTFLG }];  #IO_L24N_T3_34
#set_property -dict { PACKAGE_PIN T19   IOSTANDARD LVCMOS33 } [get_ports { G_LD }];      #IO_25_34





