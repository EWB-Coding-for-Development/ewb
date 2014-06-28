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

class SubprocessError(BaseException):
    pass

class RadioNotRunningError(SubprocessError):
   pass

class Radio(threading.Thread):
    def __init__(self, frequency, stereo=None, sample_rate=22050):
        threading.Thread.__init__(self)
        self.daemon = True
        assert(FREQUENCY_MIN < frequency < FREQUENCY_MAX)
        self.frequency = frequency
        if stereo == None:
            stereo = False
        self.stereo = stereo
        if sample_rate == None:
            sample_rate = 22050
        self.sample_rate = int(sample_rate)
        self.wav_pipe_r, self.wav_pipe_w = os.pipe()

    def run(self):
        try:
            while True:
                args = ["pifm", "-", str(self.frequency)]
                if self.sample_rate:
                    args.append(str(self.sample_rate))
                if self.stereo:
                    args.append("stereo")

                self.fm_process = subprocess.Popen(args, stdin=self.wav_pipe_r)
                retcode = self.fm_process.wait()
                if retcode == 255:
                    # pifm failed to open /dev/mem
                    raise SubprocessError("User does not have write access to /dev/mem")

        except OSError as e:
            if e.errno == 2 and not e.filename:
                e.filename = args[0] # give a more descriptive file-not-found error on Python2.x
            raise(e)

    def __repr__(self):
        if self.is_alive():
            return "<Radio: {}MHz {}KHz {}>".format(self.frequency, self.sample_rate, "stereo" if self.stereo else "mono")
        else:
            return "<Radio: Off>"

    def get_input_pipe(self):
        return self.wav_pipe_w

    def say(self, say_text, language="en", gender="male", variant=0, capital_emphasis=None,
        pitch=None, speed=None, gap=None, amplitude=None, extra_args=None,
        stdout=None, wav_fp=None, add_silence=True):

        if self.is_alive():
            say(say_text, language=language, gender=gender, variant=variant, 
                pitch=pitch, speed=speed, gap=gap, amplitude=amplitude, extra_args=extra_args,
                    capital_emphasis=capital_emphasis, stdout=self.wav_pipe_w)

            # Play a sample of silence, to prevent pifm from looping buffer
            if add_silence:
                self.play_silence()
        else:
            raise RadioNotRunningError

    def play(self, wav, add_silence=True):
        if self.is_alive():
            if hasattr(wav, 'read'):
                raise NotImplemented
            else:
                try:
                    player = subprocess.Popen(['sox', wav, '-r', '{}'.format(self.sample_rate), '-b', '16', '-t', 'wav', '-'], stderr=subprocess.PIPE, stdout=self.wav_pipe_w)
                    out, err = player.communicate()
                    if player.poll():
                        raise SubprocessError(err)
                except OSError as e:
                    if e.errno == 2 and not e.filename:
                        e.filename = 'sox' # give a more descriptive file-not-found error on Python2.x
                    raise e
            if add_silence:
                self.play_silence()
        else:
            raise RadioNotRunningError

    def play_silence(self):
        silence = os.path.join(os.path.dirname(__file__), "silence.wav")
        self.play(silence, add_silence=False)

    def tone(self, note, length=-1, tone_func='sin', add_silence=True):
        """Play a tone directly over the radio

        Arguments:
        `note`:         Note can be a frequency (Hz) or number of semitones
                            relative to middle A (440Hz) e.g. "%12" or "%-1".
                            Two Frequencies can be given, separated by one of
                            the characters ':', '+', '/', or '-', to generate a sweep.
        `length`:       Length (in seconds) of the generated tone. Default -1 (infinite length)
        `add_silence`:  Plays silence after tone is completed.

        """
        if self.is_alive():
            try:
                if length == -1:
                    length = ""
                args = ['sox', '-n', '-b', '16', '-t', 'wav', '-',
                        'synth', str(length), tone_func, str(note)]
                player = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=self.wav_pipe_w)
                out, err = player.communicate()
                if player.poll():
                    raise SubprocessError(err)
            except OSError as e:
                if e.errno == 2 and not e.filename:
                    e.filename = 'sox' # give a more descriptive file-not-found error on Python2.x
                raise e
            if add_silence:
                self.play_silence()
        else:
            raise RadioNotRunningError

    def terminate(self):
        try:
            self.fm_process.terminate()
            global _radio
            _radio = None
        except OSError:
            pass

global _radio
_radio = None

def get_radio(frequency, stereo=None, sample_rate=None, force=False):
    """Starts a Raspberry Pi `pifm` radio tuned to `frequency` MHz

    Get a radio tuned to 87.9 MHz
    >>> radio = get_radio(87.9)
    >>> radio
    <Radio: 87.9MHz 22050KHz mono>

    Broadcast "Hello World" using text-to-speech
    >>> radio.say("Hello World!")

    Play a WAV audio file
    >>> radio.play("/usr/share/pyshared/pygame/examples/data/secosmic_lo.wav")

    Get a stereo radio, tuned to 107.5 MHz at a sample rate of 44100
    >>> radio = get_radio(107.5, True, 44100)
    >>> radio
    <Radio: 107.5MHz 44100KHz stereo>

    >>> radio.frequency
    107.5
    >>> radio.stereo
    True
    >>> radio.sample_rate
    44100

    Returns <Radio>"""

    global _radio

    try:
        # if there is already a Radio, but the settings have changed, kill it.
        if _radio.frequency != frequency:
            _radio.terminate()
        if _radio.stereo != stereo:
            _radio.terminate()
        if _radio.sample_rate != sample_rate:
            _radio.terminate()

        # if `force` is set, kill the existing radio
        if force:
            _radio.terminate()
    except AttributeError:
        pass

    # Start a Radio if we don't have one
    if _radio == None:
        _radio = Radio(frequency, stereo, sample_rate)
        _radio.start()

    if _radio.is_alive():
        return _radio
    else:
        print("Radio initialisation failed")
        return None

def kill_children():
    """Handler to kill child processes at exit"""
    time.sleep(1) # wait a second so the audio transmission completes
    try:
        _radio.terminate()
    except AttributeError:
        # radio not initialised, nothing to terminate
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()

atexit.register(kill_children)
