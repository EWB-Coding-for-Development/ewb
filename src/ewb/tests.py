import unittest

from time import sleep
from ewb.radio import get_radio, RadioNotRunningError


class RadioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.radio = get_radio(87.9)

    def test_say(self):
        self.radio.say("This is a test broadcast")
        sleep(2)

    def test_play(self):
        self.radio.play("/home/pi/left_right.wav")

    def test_tone(self):
        self.radio.tone(440, length=1)
        sleep(1)

        self.radio.tone("%12", length=1)
        sleep(1)

    def test_silence(self):
        self.radio.play_silence()

    def test_say_2(self):
        self.radio.say("Goodbye")
        sleep(1)

    def test_zterminate(self):
        self.radio.terminate()
        self.assertRaises(RadioNotRunningError, self.radio.say("don't say this"))

