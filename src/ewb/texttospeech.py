# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file

import subprocess
import os

def say(say_text, language="en", gender="male", variant=0, capital_emphasis=None,
        pitch=None, speed=None, gap=None, amplitude=None, extra_args=None,
        stdout=None, wav_fp=None):
    args = ["espeak"]

    # set up voice
    if gender.lower() in ["m", "male"]:
        gender = "m"
    elif gender.lower() in ["f","female"]:
        gender = "f"
    if not variant:
        variant = ""
    voice = "-v{lang}+{gender}{variant}".format(lang=language, gender=gender, variant=variant)
    args.append(voice)

    # additional options
    if capital_emphasis:
        args.append("-k {}".format(capital_emphasis))
    if pitch:
        args.append("-p {}".format(pitch))
    if speed:
        args.append("-s {}".format(speed))
    if amplitude:
        args.append("-a {}".format(amplitude))
    if wav_fp:
        args.append("-w {}".format(wav_fp))
    if extra_args:
        args.append(extra_args)

    if stdout == None:
        stdout = subprocess.PIPE
    else:
        args.append("--stdout")

    try:
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=stdout,
               stderr=subprocess.PIPE)
        (output, err) = p.communicate(input=say_text.encode("utf-8"))
    except OSError as e:
        if e.errno == 2: # No such file or directory
            print("espeak not found. Please install espeak\n")
            e.filename = args[0]
            raise(e)
    return

if __name__ == "__main__":
    say("Hello from Python")
