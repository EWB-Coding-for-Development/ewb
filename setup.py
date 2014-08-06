#!/usr/bin/env python

from distutils.core import setup

setup (name = "EWB",
    version = "0.1a",
    description = "Engineering Without Borders 'Coding for Development' module",
    author = "James Utter",
    author_email =  "james.utter@gmail.com",
    license = ("LGPL", "CC_BY_SA"),
    url = "https://github.com/EWB-Coding-for-Development/ewb",
    keywords = ['RaspberryPi', 'FM Transmitter', 'Text To Speech', 'GPS'],
    package_dir = {'':'src'},
    packages = ['ewb'],
)

