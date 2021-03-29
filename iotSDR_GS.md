
# iotSDR Getting Started Guide
------------------------------

As you got your iotSDR, this small guide will help you setup your board to get started with the jupyter notebook

## Pre-requisites
-----------------
        1. iotSDR-7010 or 7020 board
        2. Computer with compatible browser (Google Chrome)
        3. Ethernet cable  (100M or 1G)
        4. Micro USB data cable OR Power Adapter of 5V for Power Jack
        5. Micro-SD card(class 10) with preloaded image (16GB recommended)

## MicroSD Card Setup
---------------------

To flash iotSDR Micro-SD card folow below steps:

  1. Download the appropriate iotSDR image for your board
  2. [iotSDR7010](https://bit.ly/2PEP3Y4) [iotSDR7020](https://bit.ly/3cxjA33)
  4. Use Etcher Utility [Ether](https://www.balena.io/etcher/)
  5. following the Ether instructions Write the image to a blank Micro SD card (16GB recommended)
   
if you are facing issues you can find the detailed instructions [here](https://github.com/embedinn/iotSDR/blob/master/iotSDR_uSD_Card.md)

## Board Setup
--------------
 

        Set the ** Boot** jumper to the SD position. (This sets the board to boot from the Micro-SD card)

![image](https://user-images.githubusercontent.com/11763512/112713740-7d4a7f80-8ef8-11eb-90dc-c012d78781d4.png)

        Insert the Micro SD card with respective pre-loaded iotSDR image file into the Micro SD card slot 
        Connect the  Ethernet cable, one end with iotSDR and other with PC
        Connect the USB cable to your PC/Laptop, and to the PWR + UART MicroUSB port 
        on the board (next to power jack)   
        iotSDR Board should now power up and get into boot sequence

## Running Jupyter On the iotSDR

After setting the SD card header position, inserting the SD card with pre-loaded image file, and the USB cable is connected, the green LED will come on immediately to confirm that the board has power. 

Following to that, after few seconds, the Blue / Done LED should light up to show that bit file is loaded in the Zynq® device. 

After some time you should see Green LEDs on one side of the board flash simultaneously. The system is now booted and ready for use.


    Once board setup up is complete, you can connect your browser to it to start using Jupyter notebook. 
    
    Follow the below procedure to configure ethernet connection between Host PC and iotSDR before running Jupyter notebbok on browser

    Connect board with browser (Static IP):

            Assign your computer a static IP address from the pool of 192.168.2.xx (except .99 and .1)
            Connect the board to your computer’s Ethernet port 
            ping to http://192.168.2.99 to confirm that you are connected
            Now open and browse and write 192.168.2.99:9090 in the search bar
            An enter password window will appear
            The password is: xilinx


        The board currently have a fixed IP address mode.

Once the board is connected to host, the jupyter notbook can be accessed through browser, for which a comprehensive guide can be found on the [PYNQ Website](https://pynq.readthedocs.io/en/v2.3/jupyter_notebooks.html)

## Running Application on Jupyter Notebook
After the password tab window, two folder of the notebooks on the left of webpage will appear and the files can be accessed and user can run the demo projects.
