# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
    Project Edenbridge
    Copyright (C) 2019  Zhengyu Peng

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from threading import Thread
import time
import picamera
import datetime

class Camera(Thread):
    def __init__(self, config, motion2camera, camera2bot):
        Thread.__init__(self)
        self.motion2camera = motion2camera
        self.camera2bot = camera2bot

        self.camera = picamera.PiCamera(resolution=(1024, 768))
        self.camera.start_preview()
        time.sleep(2)

    def run(self):
        while True:
            # retrieve data (blocking)
            motion_command = self.motion2camera.get()
            if motion_command is 'capture_jpg':
                print('Capturing photo')
                datetime_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                self.camera.capture('./photos/' + datetime_str + '.jpg')
                self.camera2bot.put('./photos/' + datetime_str + '.jpg')