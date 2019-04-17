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


import time
import RPi.GPIO as GPIO

def motion(config, output_queue):

    motion_pin = config['motion_pin']
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motion_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def motion_handle(pin):
        if GPIO.input(motion_pin):
            output_queue.put('Motion detected')
        else:
            output_queue.put('No motion')
    
    
    GPIO.add_event_detect(
        motion_pin, GPIO.BOTH, callback=motion_handle, bouncetime=300)
    
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