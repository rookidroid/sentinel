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
import json
import socket

from pathlib import Path
import os
import datetime

import subprocess

import copy
import logging

import time

logging.basicConfig(
    filename='/home/pi/sentinel/camera.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class Camera():
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, config):

        self.video_path = Path(config['video_path'])
        self.photo_path = Path(config['photo_path'])

        self.camera_config = config['camera']

        self.max_photo_count = self.camera_config['max_photo_count']
        self.period = self.camera_config['period']
        self.video_length = self.camera_config['video_length']

        self.det_resolution = self.camera_config['detection_resolution']
        self.rec_resolution = self.camera_config['record_resolution']

        self.delta_thresh = self.camera_config['delta_thresh']
        self.min_area = self.camera_config['min_area']
        self.motion_frame_counter = 0

        self.ip = '127.0.0.1'
        self.port = self.camera_config['listen_port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(3)
        self.signal = self.SIG_NORMAL

        self.bot_port = config['bot']['listen_port']
        self.cloud_port = config['cloud']['listen_port']

        try:
            os.makedirs(self.video_path)
        except FileExistsError:
            pass

        try:
            os.makedirs(self.photo_path)
        except FileExistsError:
            pass

        self.cmd_upload_h264 = {
            'cmd': 'upload_file',
            'file_type': 'H264',
            'file_name': '',
            'extension': '.h264',
            'date': '',
            'time': ''
        }

        self.cmd_send_jpg = {
            'cmd': 'send_photo',
            'file_type': 'JPG',
            'file_name': '',
            'extension': '.jpg',
            'date': '',
            'time': '',
            'server': ''
        }

    def take_photo(self, counts):
        if counts == 0 or counts > self.max_photo_count:
            counts = self.max_photo_count

        for photo_idx in range(0, counts):
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.datetime.now().strftime('%H-%M-%S')

            self.cmd_send_jpg['date'] = date_str
            self.cmd_send_jpg['time'] = time_str
            self.cmd_send_jpg[
                'file_name'] = date_str + '_' + time_str + '_' + 'photo' + str(
                    photo_idx)
            self.cmd_send_jpg['server'] = 'telegram'

            subprocess.call(["libcamera-still", "-o",
                             str(self.photo_path /
                                 (self.cmd_send_jpg['file_name'] + self.cmd_send_jpg['extension'])),
                             "--shutter", "100000",
                             "--gain", "1",
                             "--awbgains", "1,1",
                             "--immediate"])

            self.send_bot(copy.deepcopy(self.cmd_send_jpg))

    def take_video(self, init_photo=False):
        self.camera.resolution = self.rec_resolution

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        self.cmd_upload_h264['file_name'] = time_str + '_' + 'video' + str(0)
        self.cmd_upload_h264['date'] = date_str
        self.cmd_upload_h264['time'] = time_str

        self.cmd_send_jpg[
            'file_name'] = date_str + '_' + time_str + '_' + 'photo' + str(0)
        self.cmd_send_jpg['date'] = date_str
        self.cmd_send_jpg['time'] = time_str
        self.cmd_send_jpg['server'] = 'email'

        self.camera.start_recording(str(self.video_path /
                                        (self.cmd_upload_h264['file_name'] +
                                         self.cmd_upload_h264['extension'])))
        if init_photo:
            self.camera.capture(str(self.photo_path /
                                    (self.cmd_send_jpg['file_name'] +
                                     self.cmd_send_jpg['extension'])),
                                use_video_port=True)
            # self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))
            self.send_bot(copy.deepcopy(self.cmd_send_jpg))

        for photo_idx in range(0, int(self.video_length / self.period)):
            time.sleep(self.period)
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.datetime.now().strftime('%H-%M-%S')
            self.cmd_send_jpg['file_name'] = date_str + \
                '_' + \
                time_str + \
                '_' + \
                'photo' + \
                str(
                int(1 + photo_idx))
            self.cmd_send_jpg['date'] = date_str
            self.cmd_send_jpg['time'] = time_str
            self.cmd_send_jpg['server'] = 'email'
            self.camera.capture(str(self.photo_path /
                                    (self.cmd_send_jpg['file_name'] +
                                     self.cmd_send_jpg['extension'])),
                                use_video_port=True)

            self.send_bot(copy.deepcopy(self.cmd_send_jpg))

        self.camera.stop_recording()

        self.send_cloud(copy.deepcopy(self.cmd_upload_h264))

    def run(self):
        logging.info('Camera thread started')
        try:
            self.udp_socket.bind((self.ip, self.port))
        except OSError as err:
            # self.status.emit(self.STOP, '')
            # print('stopped')
            logging.error(err)
        else:
            # self.status.emit(self.LISTEN, '')
            # print('listen')
            while True:
                if self.signal == self.SIG_NORMAL:
                    # self.status.emit(self.LISTEN, '')
                    try:
                        data, addr = self.udp_socket.recvfrom(4096)
                    except socket.timeout as t_out:
                        # print('timeout')
                        # logging.info('timeout')
                        pass
                    else:
                        if data:
                            # print(data.decode())
                            msg = json.loads(data.decode())
                            # logging.info(data.decode())
                            if msg['cmd'] == 'take_photo':
                                # self.q2camera.task_done()
                                self.take_photo(msg['count'])
                                logging.info('Start to capture photos')
                            elif msg['cmd'] == 'take_video':
                                # self.q2camera.task_done()
                                self.take_video(init_photo=True)
                                logging.info('Start to record videos')
                        else:
                            # self.status.emit(self.LISTEN, '')
                            break
                elif self.signal == self.SIG_STOP:
                    self.signal = self.SIG_NORMAL
                    self.udp_socket.close()
                    # self.status.emit(self.LISTEN, '')
                    break
        finally:
            # print('stopped')
            logging.info('camera UDP stopped')
            # self.status.emit(self.STOP, '')

    def send_bot(self, msg):
        payload = json.dumps(msg)
        self.udp_socket.sendto(payload.encode(), ('127.0.0.1', self.bot_port))

    def send_cloud(self, msg):
        payload = json.dumps(msg)
        self.udp_socket.sendto(
            payload.encode(), ('127.0.0.1', self.cloud_port))


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    # config = json.load(open('./front_door.json'))

    camera = Camera(config)
    camera.run()


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
