import RPi.GPIO as GPIO 
import time

# Define a function named blink()
def blink(count, period, pin_num=11):
  '''outputs blinks to an LED via a GPIO pin (default pin 11)
  count = number of LED blinks
  period = number of seconds for each LED blink
  pin_num = GPIO pin number to output to'''
  # Use board pin numbering
  GPIO.setmode(GPIO.BOARD)
  # Setup GPIO pin 'pin_num' to OUT
  GPIO.setup(pin_num, GPIO.OUT)
  # Loop through LED blink 'count' times 
  for i in range(0, count):
    print "Iteration " + str(i+1) + " of " + str(count)
    # pin 'pin_num' ON
    GPIO.output(pin_num,True)
    # wait 'period' seconds
    time.sleep(period)
    # pin 'pin_num'  OFF
    GPIO.output(pin_num,False)
    # wait 'period' seconds
    time.sleep(period)
  print "Done"
  # Reset status GPIO pins
  GPIO.cleanup()

