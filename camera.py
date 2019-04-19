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
import queue
import logging


class Camera(Thread):
    def __init__(self, config, motion2camera, camera2mbot):
        Thread.__init__(self)
        self.motion2camera = motion2camera
        self.camera2mbot = camera2mbot
        self.camera = picamera.PiCamera(resolution=(1280, 960))
        self.max_frames = 10

    def capture_jpg(self, frames, period):
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        try:
            for frame_idx, filename in enumerate(
                    self.camera.capture_continuous(
                        './photos/image{counter:02d}' + '_' + datetime_str +
                        '.jpg')):

                if (frame_idx >= frames
                        and frames > 0) or (frame_idx >= self.max_frames):
                    logging.warning('Reach to maximum frame')
                    break

                logging.info('Capture ' + filename)
                self.camera2mbot.put(filename)

                try:
                    motion_command = self.motion2camera.get(
                        block=True, timeout=period)
                except queue.Empty:
                    # Handle empty queue here
                    pass
                else:
                    if motion_command is 'stop_capture_jpg':
                        self.motion2camera.task_done()
                        logging.info('Stop capturing')
                        break
                    else:
                        self.motion2camera.task_done()
                        logging.warning('Wrong command, continue capturing')
        finally:
            pass

    def run(self):
        logging.info('Camera thread started')
        while True:
            # retrieve data (blocking)
            motion_command = self.motion2camera.get()
            if motion_command is 'capture_jpg':
                self.motion2camera.task_done()
                self.capture_jpg(0, 30)
                logging.info('Start to capture photos')

            else:
                self.motion2camera.task_done()


'''

    `                      `
    -:.                  -#:
    -//:.              -###:
    -////:.          -#####:
    -/:.://:.      -###++##:
    ..   `://:-  -###+. :##:
           `:/+####+.   :##:
    .::::::::/+###.     :##:
    .////-----+##:    `:###:
     `-//:.   :##:  `:###/.
       `-//:. :##:`:###/.
         `-//:+######/.
           `-/+####/.
             `+##+.
              :##:
              :##:
              :##:
              :##:
              :##:
               .+:

'''