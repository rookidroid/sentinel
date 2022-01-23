#!/usr/bin/env python3
"""
    Project Edenbridge
    Copyright (C) 2019 - 2022  Zhengyu Peng

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

import argparse
import time
import json
# import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import socket
import datetime

import logging
logging.basicConfig(
    filename='/home/pi/sentinel/motion.log', level=logging.INFO)


class Motion():
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, config):

        self.camera_port = config['camera']['listen_port']
        self.bot_port = config['bot']['listen_port']

        self.ip = '127.0.0.1'
        self.port = config['motion']['listen_port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.motion_pin = config['motion']['pir_pin']

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.motion_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pir = MotionSensor(self.motion_pin)
        # GPIO.setup(self.enable_pin, GPIO.OUT, initial=GPIO.HIGH)

    def send_udp(self, msg, port):
        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = json.dumps(msg)
        self.udp_socket.sendto(payload.encode(), ('127.0.0.1', port))

    def run(self):
        # print('Motion thread started')
        logging.info('Motion thread started')

        while True:
            self.pir.wait_for_motion()
            print('motion detected')
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.datetime.now().strftime('%H-%M-%S')
            self.send_udp({'cmd': 'take_photo', 'count': 1}, self.camera_port)

            self.send_udp({
                'cmd': 'send_msg',
                'date': date_str,
                'time': time_str
            }, self.bot_port)
            # print('motion detected')
            logging.info('motion detected')

            self.pir.wait_for_no_motion()
            logging.info('no motion')
            # time.sleep(1e6)


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    motion = Motion(config)
    motion.run()


if __name__ == '__main__':
    main()

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
