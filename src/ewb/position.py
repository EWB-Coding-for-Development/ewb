# Copyright (c) 2014 James Utter, All rights reserved.
#
# @author: see AUTHORS file

import gps

import threading
import time

class GPS(gps.gps, threading.Thread):
    def __init__(self, *args, **kwargs):
        """Wrapper around gps.gps

        Continously updates in the background, rather than requiring polling.
        """
        gps.gps.__init__(self, *args, **kwargs)

        if len(args) < 4 and "mode" not in kwargs:
            self.stream(gps.WATCH_ENABLE)

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.last_update = self.next()
            self.last_update_time = time.time()

    def get_map_url(self, z=18, service='google'):
        if service == 'google':
            return "https://www.google.com.au/maps/@{fix.latitude},{fix.longitude},{zoom}z".format(fix=self.fix, zoom=z)
        elif service == 'openstreetmap':
            return "http://www.openstreetmap.org/#map={zoom}/{fix.latitude}/{fix.longitude}".format(fix=self.fix, zoom=z)
        else:
            raise NotImplementedError("Service '{}' Not Implemented".format(service))
