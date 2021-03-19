# iotSDR Getting Started Guide

## Prerequisites

        iotSDR-7010 ot 7020 board
        Computer with compatible browser (Supported Browsers)
        Ethernet cable
        Micro USB cable
        Micro-SD card with preloaded image, or blank card (Minimum 8GB recommended)


## Board Setup

        .. 

        Set the ** Boot** jumper to the SD position. (This sets the board to boot from the Micro-SD card)
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

            Assign your computer a static IP address
            Connect the board to your computer’s Ethernet port
            Browse to http://192.168.2.99

    If you connect to a router, or a network with a DHCP server, your board will automatically get an IP address. You must make sure you have permission to connect a device to your network, otherwise the board may not connect properly.

    Connect to a Router/Network (DHCP):

            Connect the Ethernet port on your board to a router/switch
            Connect your computer to Ethernet or WiFi on the router/switch
            Browse to http://<board IP address>
            Optional: Change the Hostname
            Optional: Configure Proxy Settings

