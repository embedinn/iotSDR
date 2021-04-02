# ZYNQ firmware development 

supported Version: Vivado 2019.1

## Generate Vivado Project
    $ git clone  https://github.com/archy-embedinn/iotSDR_Platform.git
    $ cd iotSDR

    good way is to fork the repo in your git account, git clone your own forked repo in your system 
    make changes in your forked repo do commits and when verified make pull request to upstream repo
    
    - open vivado
    - make sure you are in source directory i.e "/home/foo/..../iotSDR/boards/iotSDR-GPS_Z7010" 
    - in tcl window
        $ cd /home/foo/..../iotSDR/boards/iotSDR-GPS_Z7010
        $ source ./write_project.tcl
    - if iotSDR-GPS_Z7010_pynq
    this will create new project and run synth/imp/bitfile and generate bitfile    

### Customize Vivado Project
    - When vivado design changes are updated and verified bitfile generation
    - make sure you are in source directory i.e "/home/foo/..../iotSDR/boards/iotSDR-GPS_Z7010"
    - make sure your bd is open in vivado project

    - in tcl window
        $ write_bd_tcl -force ./block_design.tcl    
    Note: its necessarry to delete iotSDR_pynq project directry if you want to create project again 
        $ rm -r ./iot_SDR_pynq     
        and then source write_project.tcl

### Build project from commandline        
    $ cd iotSDR_Platform/boards/iotSDR-GPS_Z7010/
    $ source <Xilinx_dir>/Vivado/2019.1/settings64.sh
    $ make
      or
    $ vivado -mode batch -nojournal -nolog -source write_project.tcl
