import RPi.GPIO as GPIO 
import time

# Define a function named blink()
def blink(count, period):
  '''outputs a loop of blinks to an LED via GPIO pin 7
  count = number of LED blinks
  period = number of seconds for each LED blink'''
  # Set pin number 'pin_num' to output to
  pin_num = 7
  # Use board pin numbering
  GPIO.setmode(GPIO.BOARD)
  # Setup GPIO pin 7 to OUT
  GPIO.setup(pin_num, GPIO.OUT)
  # Loop through LED blink 'count' times 
  for i in range(0, count):
    print "Iteration " + str(i+1)
    # pin 7 ON
    GPIO.output(pin_num,True)
    # wait 'period' seconds
    time.sleep(period)
    # pin 7 OFF
    GPIO.output(pin_num,False)
    # wait 'period' seconds
    time.sleep(period)
  print "Done"
  # Reset status GPIO pins
  GPIO.cleanup()

