ewb
===

This module is for use with the Engineers-Without-Borders "Coding for Development" classes.
It contains several modules for use with a RaspberryPi.

## Modules

ewb.radio: An interface to the `pifm` FM transmitter. Includes Text-to-speech capability
ewb.position: An interface to the GPS
ewb.blink: Introductory functions for the accessing the Inputs and Outputs of the RaspberryPi

## Dependencies

* pifm

    cd ~
    wget http://omattos.com/pifm.tar.gz
    tar xf pifm.tar.gz
    sudo mv pifm /usr/sbin/pifm

* ipython
* ipython-notebook
* python-gps
* python-rpi.gpio
* espeak
* git

    apt-get install ipython-notebook python-gps python-rpi.gpio espeak git

## How to download and run this code

On your raspberry pi:

First find the IP ADDRESS of your Raspberry Pi. Paste the following into the command line of your Pi:

    ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'

It should print out an address such as 192.168.0.2

Now download this code into your home directory

    cd ~
    git clone git@github.com:EWB-Coding-for-Development/ewb.git

If you are connecting the GPS directly to the Pi, the following is required to disable the Serial Console

    sudo patch -p0 < ewb/disable_serial_console

Then to start the Notebook server, run:

    sudo ipython notebook --ip=* ewb/notebooks

Finally, on your computer, open a browser and navigate to http://IP ADDRESS:8888 or http://raspberrypi:8888
