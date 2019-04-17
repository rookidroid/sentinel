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
import RPi.GPIO as GPIO


class Motion(Thread):
    def __init__(self, config, output_queue):
        Thread.__init__(self)
        self.motion_pin = config['motion_pin']
        self.output_queue = output_queue

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def motion_handle(self, pin):
        if GPIO.input(pin):
            self.output_queue.put('capture_jpg')
            print('Motion detected')
        else:
            self.output_queue.put('stop_capture_jpg')
            print('No motion')

    def run(self):
        GPIO.add_event_detect(
            self.motion_pin,
            GPIO.BOTH,
            callback=self.motion_handle,
            bouncetime=300)

        while True:
            time.sleep(1e6)


'''
    Z. Peng

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