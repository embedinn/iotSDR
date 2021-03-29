

set_property PACKAGE_PIN T16 [get_ports {LED[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LED[0]}]

set_property PACKAGE_PIN Y16 [get_ports {LED1[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LED1[0]}]



set_property PACKAGE_PIN U15 [get_ports SPI0_SCLK_O_0]
set_property PACKAGE_PIN U13 [get_ports SPI0_MISO_I_0]
set_property PACKAGE_PIN U12 [get_ports SPI0_MOSI_O_0]
set_property PACKAGE_PIN Y14 [get_ports SPI0_SS_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_MISO_I_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_MOSI_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_SCLK_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI0_SS_O_0]

set_property PACKAGE_PIN V12 [get_ports SPI1_MOSI_O_0]
set_property PACKAGE_PIN V13 [get_ports SPI1_MISO_I_0]
set_property PACKAGE_PIN U14 [get_ports SPI1_SCLK_O_0]
set_property PACKAGE_PIN T15 [get_ports SPI1_SS_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_MISO_I_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_MOSI_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SCLK_O_0]
set_property IOSTANDARD LVCMOS33 [get_ports SPI1_SS_O_0]

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



#set_property LOC IDELAYCTRL_X0Y0 [get_cells design_1_i/TRX_CH2/LVDS_IO_TRX_0/inst/delayctrl]
#set_property LOC IDELAYCTRL_X0Y0 [get_cells design_1_i/TRX_CH1/LVDS_IO_TRX_0/inst/delayctrl]

set_property C_CLK_INPUT_FREQ_HZ 300000000 [get_debug_cores dbg_hub]
set_property C_ENABLE_CLK_DIVIDER false [get_debug_cores dbg_hub]
set_property C_USER_SCAN_CHAIN 1 [get_debug_cores dbg_hub]
connect_debug_port dbg_hub/clk [get_nets clk]
