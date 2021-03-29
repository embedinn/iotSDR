# Vivado 2019.1
# iotSDR GPS Design

set origin_dir "."
catch {launch_runs impl_1 -to_step write_bitstream jobs -6}
catch {wait_on_run impl_1}
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.bit $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.bit
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.srcs/sources_1/bd/design_1/hw_handoff/design_1.hwh $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.hwh
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.ltx $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.ltx

