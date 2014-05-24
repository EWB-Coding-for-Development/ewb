blink-led
=========

Simple script for outputting a blinking LED from a Raspberry Pi GPIO pin. Inpsired by Scott Mangold's article 'Lighting Up An Led Using Your Raspberry Pi and Python' (http://www.thirdeyevis.com/pi-page-2.php)

Dependancies:
raspberry-gpio-python
$ sudo apt-get update
$ sudo apt-get dist-upgrade
$ sudo apt-get install python-rpi.gpio python3-rpi.gpio

When blink.py is either imported or executed within the python/ipython shell, the 'blink()' function is defined:
blink(count, period)
'''outputs a loop of blinks to an LED via GPIO pin 7
  count = number of LED blinks
  period = number of seconds for each LED blink'''

eg running 'blink(5,1)' will make the LED blink 5 times, holding for 1 second per blink.
