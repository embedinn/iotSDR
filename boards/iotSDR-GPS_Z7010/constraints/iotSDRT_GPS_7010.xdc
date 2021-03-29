# RFIC Ch1 SPI Connections
set_property PACKAGE_PIN U15 [get_ports SPI0_SCLK_O_0]
set_property PACKAGE_PIN U13 [get_ports SPI0_MISO_I_0]
set_property PACKAGE_PIN U12 [get_ports SPI0_MOSI_O_0]
set_property PACKAGE_PIN Y14 [get_ports SPI0_SS_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_MISO_I_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_MOSI_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_SCLK_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_SS_O_0]

## RFIC Ch2 SPI Connections / Disconected internally
#set_property PACKAGE_PIN V12 [get_ports SPI1_MOSI_O_0]
#set_property PACKAGE_PIN U14 [get_ports SPI1_SCLK_O_0]
#set_property PACKAGE_PIN T15 [get_ports SPI1_SS_O_0]
#set_property IOSTANDARD LVCMOS33 [get_ports SPI1_MISO_I_0]
#set_property IOSTANDARD LVCMOS33 [get_ports SPI1_MOSI_O_0]
#set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SCLK_O_0]
#set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SS_O_0]

#GPS SPI connections
set_property PACKAGE_PIN Y19 [get_ports SPI1_MOSI_O_GPS]
set_property PACKAGE_PIN N18 [get_ports SPI1_SCLK_O_GPS]
set_property PACKAGE_PIN W16 [get_ports SPI1_SS_O_GPS]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_MOSI_O_GPS]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SCLK_O_GPS]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SS_O_GPS]

#GPS IQ Interface
set_property PACKAGE_PIN R16 [get_ports G_I0]
set_property PACKAGE_PIN T17 [get_ports G_Q0]
set_property PACKAGE_PIN R17 [get_ports G_I1]
set_property PACKAGE_PIN P15 [get_ports G_Q1]

set_property PACKAGE_PIN T19 [get_ports G_LD]
set_property PACKAGE_PIN W20 [get_ports G_IDLE]
set_property PACKAGE_PIN Y18 [get_ports G_SHDN]
set_property PACKAGE_PIN V16 [get_ports G_PGM]
set_property PACKAGE_PIN P16 [get_ports G_ANT_FLG]
set_property PACKAGE_PIN P19 [get_ports G_CLKOUT]

set_property IOSTANDARD LVCMOS33 [get_ports G_PGM]
set_property IOSTANDARD LVCMOS33 [get_ports G_ANT_FLG]
set_property IOSTANDARD LVCMOS33 [get_ports G_CLKOUT]
set_property IOSTANDARD LVCMOS33 [get_ports G_I0]
set_property IOSTANDARD LVCMOS33 [get_ports G_I1]
set_property IOSTANDARD LVCMOS33 [get_ports G_LD]
set_property IOSTANDARD LVCMOS33 [get_ports G_Q0]
set_property IOSTANDARD LVCMOS33 [get_ports G_Q1]
set_property IOSTANDARD LVCMOS33 [get_ports G_IDLE]
set_property IOSTANDARD LVCMOS33 [get_ports G_SHDN]

#CH1 Transmitter
set_property PACKAGE_PIN J20 [get_ports {txd_p_0[0]}]
set_property PACKAGE_PIN K17 [get_ports txclk_p_0]
#CH1 Receievr
set_property PACKAGE_PIN J18 [get_ports rxclk_p_0]
set_property PACKAGE_PIN G19 [get_ports {rxd_p_0[0]}]
set_property PACKAGE_PIN G17 [get_ports {rxd24_p_0[0]}]



#CH2 Transmitter
set_property PACKAGE_PIN H16 [get_ports txclk_p_1]
set_property PACKAGE_PIN D19 [get_ports {txd_p_1[0]}]
#CH2 Receiver
set_property PACKAGE_PIN L16 [get_ports rxclk_p_1]
set_property PACKAGE_PIN E18 [get_ports {rxd_p_1[0]}]
set_property PACKAGE_PIN B19 [get_ports {rxd24_p_1[0]}]

#LEDs TXRX  for test
#set_property PACKAGE_PIN T16 [get_ports led_0]
#set_property PACKAGE_PIN Y16 [get_ports led_1]
#set_property IOSTANDARD LVCMOS33 [get_ports led_0]
#set_property IOSTANDARD LVCMOS33 [get_ports led_1]

set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets G_CLKOUT_IBUF]


set_property IOSTANDARD LVCMOS33 [get_ports {leds_6bits_tri_o[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {leds_6bits_tri_o[4]}]
