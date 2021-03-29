# Vivado 2019.1
# iotSDR GPS Design

set origin_dir "."
set iprepo_dir $origin_dir/../ip

create_project iotSDR_GPS $origin_dir/iotSDR_GPS_pynq -part xc7z020clg400-1
set_property board_part embedinn:iot_7020:part0:1.2 [current_project]
set_property  ip_repo_paths $iprepo_dir [current_project]
add_files -norecurse $origin_dir/../ip/utilities/ledBlink.vhd
add_files -norecurse $origin_dir/../ip/utilities/tx_stream_mux.vhd
add_files -norecurse $origin_dir/../ip/gnss_receiver_max2769/max2769_interface.vhd
set_property target_language VHDL [current_project]
update_ip_catalog
source $origin_dir/block_design.tcl
make_wrapper -files [get_files $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.vhd
add_files -fileset constrs_1 -norecurse $origin_dir/constraints/iotSDRT_GPS_7020.xdc
update_compile_order -fileset sources_1
launch_runs impl_1 -to_step write_bitstream -jobs 6
wait_on_run impl_1
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.bit $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.bit
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.srcs/sources_1/bd/design_1/hw_handoff/design_1.hwh $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.hwh
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.ltx $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.ltx
