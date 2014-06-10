# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file

import atexit
import os
import subprocess
import sys
import threading
import time

from texttospeech import say

FREQUENCY_MIN, FREQUENCY_MAX = (76.0, 108.0)

class PermissionsError(BaseException):
    pass

class Radio(threading.Thread):
    def __init__(self, frequency, stereo=None, sample_rate=None):
        threading.Thread.__init__(self)
        self.daemon = True
        assert(FREQUENCY_MIN < frequency < FREQUENCY_MAX)
        self.frequency = frequency
        self.stereo = stereo
        self.sample_rate = sample_rate
        self.wav_pipe_r, self.wav_pipe_w = os.pipe()

    def run(self):
        try:
            args = ["pifm", "-", str(self.frequency)]
            if self.sample_rate:
                args.append(self.sample_rate)
            if self.stereo:
                args.append(self.stereo)

            self.fm_process = subprocess.Popen(args, stdin=self.wav_pipe_r)
            retcode = self.fm_process.wait()
            if retcode == 255:
                # pifm failed to open /dev/mem
                raise PermissionsError, "User does not have write access to /dev/mem"

        except OSError as e:
            # This improves the detail given by the error on Python2.x
            if e.errno == 2:
                print("File Not Found: '{}'".format(binary))
                print("Make sure {} is installed and included in your PATH\n".format(binary))
                if not e.filename:
                    e.filename = binary # give a more descriptive file-not-found message
                raise(e)

    def get_input_pipe(self):
        return self.wav_pipe_w

    def say(self, say_text, language="en", gender="male", variant=0, capital_emphasis=None,
        pitch=None, speed=None, gap=None, amplitude=None, extra_args=None,
        stdout=None, wav_fp=None, gapless=False):

        say(say_text, language=language, gender=gender, variant=variant, 
            pitch=pitch, speed=speed, gap=gap, amplitude=amplitude, extra_args=extra_args,
                capital_emphasis=capital_emphasis, stdout=self.wav_pipe_w)

        # Play a sample of silence, to prevent pifm from looping buffer
        if not gapless:
            self.play(os.path.join(os.path.dirname(__file__), "silence.wav"))

    def play(self, wav):
        player = subprocess.Popen(['cat', wav], stdout=self.wav_pipe_w)
        player.wait()

    def terminate(self):
        self.fm_process.terminate()
        _radio = None

global _radio
_radio = None

def get_radio(frequency, stereo=None, sample_rate=None):
    global _radio
    if _radio == None:
        radio = Radio(frequency, stereo, sample_rate)
        radio.start()
        _radio = radio
    return _radio

def kill_children():
    """Handler to kill child processes at exit"""
    time.sleep(0.3) # wait a fraction of a second so the audio transmission completes
    _radio.terminate()

atexit.register(kill_children)
