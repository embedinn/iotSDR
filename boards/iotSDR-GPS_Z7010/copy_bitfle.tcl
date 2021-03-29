# Vivado 2019.1
# iotSDR GPS Design bitfile to git repo

set origin_dir "."
file delete -force $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.bit
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.bit $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.bit
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.srcs/sources_1/bd/design_1/hw_handoff/design_1.hwh $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.hwh
file copy -force $origin_dir/iotSDR_GPS_pynq/iotSDR_GPS.runs/impl_1/design_1_wrapper.ltx $origin_dir/iotSDR_GPS/bitstream/iotSDR_GPS.ltx

