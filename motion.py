#!/usr/bin/env python3
"""
    Project Edenbridge
    Copyright (C) 2019 - 2020  Zhengyu Peng

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
import RPi.GPIO as GPIO
import socket

import logging
logging.basicConfig(filename='edenbridge.log', level=logging.ERROR)


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

        self.ip = '127.0.0.1'
        self.port = config['motion']['listen_port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.motion_pin = 14
        # self.enable_pin = config['enable_pin']
        # self.output_queue = output_queue
        # self.msg_capture_jpg = {'cmd': 'take_photo', 'count': 0}
        # self.cmd_take_video = {'cmd': 'take_video', 'count': 0}
        # self.msg_stop = {'cmd': 'stop', 'arg': 0}

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(self.enable_pin, GPIO.OUT, initial=GPIO.HIGH)

    def send_udp(self, msg, port):
        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = json.dumps(msg)
        self.udp_socket.sendto(payload.encode(), ('127.0.0.1', port))

    def motion_handle(self, pin):
        if GPIO.input(pin):
            # self.output_queue.put(self.cmd_take_video)
            # self.output_queue.put(self.msg_capture_jpg)
            # logging.info('Motion detected')

            self.send_udp({'cmd': 'take_photo', 'count': 1}, self.camera_port)
            # print('motion detected')
            logging.info('motion detected')

        else:
            # self.output_queue.put(self.msg_stop)
            # logging.info('No motion')
            logging.info('no motion')
            # print('no motion')

    def run(self):
        # logging.info('Motion thread started')
        # print('Motion thread started')
        logging.info('Motion thread started')
        GPIO.add_event_detect(self.motion_pin,
                              GPIO.BOTH,
                              callback=self.motion_handle,
                              bouncetime=300)

        while True:
            time.sleep(1e6)


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    # config = json.load(open('./front_door.json'))
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
