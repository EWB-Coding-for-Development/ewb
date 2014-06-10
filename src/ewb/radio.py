# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file

import os
import subprocess
import sys
import threading

from texttospeech import say

class Radio(threading.Thread):
    def __init__(self, frequency, stereo=None, sample_rate=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.frequency = frequency
        self.stereo = stereo
        self.sample_rate = sample_rate
        self.wav_pipe_r, self.wav_pipe_w = os.pipe()

    def run(self):
        try:
            cmd = ["pifm", "-", str(self.frequency)] #str(self.sample_rate), "stereo" if self.stereo else "mono"]
            print(cmd)
            self.fm_process = subprocess.Popen(cmd, bufsize=10,
                    stdin=self.wav_pipe_r)
            print("pifm started")
            self.fm_process.wait()
            print("pifm finished")
        except OSError as e:
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


global _radio
_radio = None

def get_radio(frequency, stereo=None, sample_rate=None):
    global _radio
    if _radio == None:
        radio = Radio(frequency, stereo, sample_rate)
        radio.start()
	_radio = radio
    return _radio

