# Vivado 2019.1
# iotSDR IOT Design bitfile to git repo

set origin_dir "."
file delete -force $origin_dir/iotSDR_IOT/bitstream/iotSDR_IOT.bit
file copy -force $origin_dir/iotSDR_IOT_pynq/iotSDR_IOT.runs/impl_1/design_1_wrapper.bit $origin_dir/iotSDR_IOT/bitstream/iotSDR_IOT.bit
file copy -force $origin_dir/iotSDR_IOT_pynq/iotSDR_IOT.srcs/sources_1/bd/design_1/hw_handoff/design_1.hwh $origin_dir/iotSDR_IOT/bitstream/iotSDR_IOT.hwh
file copy -force $origin_dir/iotSDR_IOT_pynq/iotSDR_IOT.runs/impl_1/design_1_wrapper.ltx $origin_dir/iotSDR_IOT/bitstream/iotSDR_IOT.ltx

