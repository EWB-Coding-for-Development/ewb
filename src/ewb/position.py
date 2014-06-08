# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file

import gps

import threading
import time
import datetime

class GpsPoller(threading.Thread):
    """Implements a thread that continuously polls the GPS for new data

    To get a GpsPoller instance, you should use get_gps()

    Inspired by: http://www.stackoverflow.com/questions/6146131/python-gps-module-reading-latest-gps-data
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps.gps(mode=gps.WATCH_ENABLE)
        self.current_value = None

    def get_current_value(self):
        return self.current_value

    def get_position(self):
        raise NotImplementedError

    def start_logging(self):
        raise NotImplementedError

    def get_log(self):
        raise NotImplementedError

    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
        except StopIteration:
            pass


class GpsLogger(threading.Thread):
    def __init__(self, period, count=None, fo=None):
        threading.Thread.__init__(self)
        self.period = period
        self.count = count
        self.gpsp = get_gps()
        self.log = []

    def get_value_to_log(self):
        return (datetime.datetime.now(), self.gpsp.get_current_value())

    def run(self):
        while (self.count == None) or (self.count > 0):
            self.log.append(self.get_value_to_log())
            if self.count != None:
                self.count += -1
            time.sleep(self.period)

    def get_log(self):
        return self.log

global _gpsp
_gpsp = None

def get_gps():
    """Returns a (singleton) GpsPoller instance.
    """
    global _gpsp
    if _gpsp == None:
        poller = GpsPoller()
        poller.start()
        _gpsp = poller
    return _gpsp
