# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file
"""ewb - Engineering without borders Python Module

classes:
    Radio
    Gps

data:
    morse_code
"""

__author__ = "James Utter"
__license__ = ("LGPL", "CC_BY_SA")
__url__ = "https://github.com/EWB-Coding-for-Development/ewb"

from ewb.position import GPS as Gps

from ewb.fm_radio import get_radio as Radio

# the following dictionary is derived from the morse package for python
# @author: Augie Fackler <durin42@gmail.com>
morse_code = {
        '!': '-.-.--',
        "'": '.----.',
        '"': '.-..-.',
        '$': '...-..-',
        '&': '.-...',
        '(': '-.--.',
        ')': '-.--.-',
        '+': '.-.-.',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '=': '-...-',
        '?': '..--..',
        '@': '.--.-.',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-',
        ' ': ' ',
        }
