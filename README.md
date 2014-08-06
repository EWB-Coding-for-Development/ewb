ewb
===

This module is for use with the Engineers-Without-Borders "Coding for Development" classes.
It contains several modules for use with a RaspberryPi.

## Modules

`ewb.radio`: An interface to the `pifm` FM transmitter. Includes Text-to-speech capability

`ewb.position`: An interface to the GPS

`ewb.blink`: Introductory functions for the accessing the Inputs and Outputs of the RaspberryPi

## Dependencies

### pifm

    cd ~  
    wget http://omattos.com/pifm.tar.gz  
    tar xf pifm.tar.gz  
    sudo cp pifm /usr/sbin/pifm

### System dependencies

    sudo apt-get install ipython-notebook python-gps python-rpi.gpio espeak git sox

Recommended but not required:

    sudo apt-get install gpsd-clients picocom libsox-fmt-all

## How to download and run this code

On your raspberry pi:
1. Download the `ewb` code. In this example, the `ewb` folder will be placed in your home directory

    cd ~  
    git clone --recursive git@github.com:EWB-Coding-for-Development/ewb.git

2. (Optional) Install the module system-wide

    sudo ./ewb/setup.py install

3.  If you are connecting the GPS directly to the Pi, the following is required to enable the serial port

    sudo patch -p0 < ewb/disable_serial_console

4. Now find the IP ADDRESS of your Raspberry Pi. It should look something like 192.168.0.2.

    # This command will print the IP ADDRESS of your Pi  
    ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'

5. To start the Notebook server, run:

    sudo ipython notebook --ip=* ewb/notebooks

6. Finally, on your computer, open a browser and navigate to http://IP ADDRESS:8888 or http://raspberrypi:8888
