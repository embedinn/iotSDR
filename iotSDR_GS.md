# iotSDR Getting Started Guide

As you got your iotSDR, this small guide will help you setup your board to get started with the jupyter notebook

## Pre-requisites

        1. iotSDR-7010 ot 7020 board
        2. Computer with a latest browser
        3. Ethernet cable
        4. Micro USB cable
        5. Micro-SD card with preloaded image, or blank card (Minimum 16GB recommended)
if you don't have Micro-SD card with image loaded, you can find the detailed instructions [here](https://github.com/embedinn/iotSDR/blob/master/iotSDR_uSD_Card.md)

## Board Setup

 

        Set the ** Boot** jumper to the SD position. (This sets the board to boot from the Micro-SD card)

![image](https://user-images.githubusercontent.com/11763512/112713740-7d4a7f80-8ef8-11eb-90dc-c012d78781d4.png)

        Insert the Micro SD card loaded with the image into the Micro SD card slot underneath the board
        Connect the Ethernet port by following the instructions below
        Connect the USB cable to your PC/Laptop, and to the PWR + UART MicroUSB port on the board
        iotSDR Board should now booted up and the boot sequence can be checked by following the instructions below

## Running Jupyter On the iotSDR

As the USB cable is connected, the green LED will come on immediately to confirm that the board has power. After a few seconds, the Blue / Done LED will light up to show that bit file is loaded in the Zynq® device.

After a minute you should see Green LEDs flash simultaneously. The system is now booted and ready for use.

    Once board setup is complete, you can connect your browdser to it to start using Jupyter notebook.

    If available, you should connect your board to a network or router with Internet access. This will allow you to update your board and easily install new packages.

    You will need to have an Ethernet port available on your computer, and you will need to have permissions to configure your network interface. With a direct connection, you will be able to use PYNQ, but unless you can bridge the Ethernet connection to the board to an Internet connection on your computer, your board will not have Internet access. You will be unable to update or load new packages without Internet access.

    Connect directly to a computer (Static IP):

            Assign your computer a static IP address from the pool of 192.168.2.xx
            Connect the board to your computer’s Ethernet port 
            Browse or ping to http://192.168.2.99 to confirm that you are connected

        The board currently have a fixed IP address mode. If you want to connect the board to a router, or a network with a DHCP server, you may follow 

Once the board is connected to host, the jupyter notbook can be accessed though browswer, for which a comprehensive guide can be found on the [PYNQ Website](https://pynq.readthedocs.io/en/v2.3/jupyter_notebooks.html)
