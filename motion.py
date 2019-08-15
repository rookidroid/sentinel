#!/usr/bin/env python3
"""
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
"""

from threading import Thread
import time
import RPi.GPIO as GPIO

import logging
logging.basicConfig(filename='edenbridge.log', level=logging.ERROR)


class Motion(Thread):
    def __init__(self, config, output_queue):
        Thread.__init__(self)
        self.motion_pin = config['motion_pin']
        self.enable_pin = config['enable_pin']
        self.output_queue = output_queue
        self.msg_capture_jpg = {'cmd': 'take_photo', 'count': 0}
        self.cmd_take_video = {'cmd': 'take_video', 'count': 0}
        self.msg_stop = {'cmd': 'stop', 'arg': 0}

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.enable_pin, GPIO.OUT, initial=GPIO.HIGH)

    def motion_handle(self, pin):
        if GPIO.input(pin):
            # self.output_queue.put(self.cmd_take_video)
            self.output_queue.put(self.msg_capture_jpg)
            logging.info('Motion detected')
            # print('motion detected')

        else:
            # self.output_queue.put(self.msg_stop)
            logging.info('No motion')
            # print('no motion')

    def run(self):
        logging.info('Motion thread started')
        GPIO.add_event_detect(self.motion_pin,
                              GPIO.BOTH,
                              callback=self.motion_handle,
                              bouncetime=300)

        while True:
            time.sleep(1e6)


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