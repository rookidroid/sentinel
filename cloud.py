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
from subprocess import call, Popen
import os
import logging

logging.basicConfig(
    filename='/home/pi/edenbridge/cloud.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class Cloud():
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

        self.target_folder = config['cloud']['folder']
        self.rclone_remote = config['cloud']['rclone_remote']

        self.camera_port = config['camera']['listen_port']
        self.bot_port = config['bot']['listen_port']
        self.cloud_port = config['cloud']['listen_port']

        self.ip = '127.0.0.1'
        self.port = config['cloud']['listen_port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(10)
        self.signal = self.SIG_NORMAL

    def h264_to_mp4(self, input, output):
        retcode = call(["MP4Box", "-add", input, output])
        if retcode != 0:
            print("Couldn't convert", input)
        else:
            os.remove(input)

    def upload_to_gdrive(self, path, metadata):
        Popen([
            "rclone", "move", path, self.rclone_remote + ':' +
            self.target_folder + '/' + metadata['date'], "--delete-after",
            "--include", metadata['file_name'] + '.mp4'
        ])

    def run(self):
        logging.info('Cloud thread started')
        try:
            self.udp_socket.bind((self.ip, self.port))
        except OSError as err:
            # self.status.emit(self.STOP, '')
            # print('stopped')
            logging.error(err)
        else:
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
                            # self.message.emit(
                            #     addr[0]+':'+str(addr[1]), data.decode())
                            # print(data.decode())
                            msg = json.loads(data.decode())
                            if msg['cmd'] is 'upload_file':
                                if msg['file_type'] is 'H264':
                                    self.h264_to_mp4(
                                        str(self.video_path / (msg['file_name'] + '.h264')),
                                        str(self.video_path / (msg['file_name'] + '.mp4')))
                                    self.upload_to_gdrive(self.video_path, msg)
                        else:
                            # self.status.emit(self.LISTEN, '')
                            break
                elif self.signal == self.SIG_STOP:
                    self.signal = self.SIG_NORMAL
                    self.udp_socket.close()
                    # self.status.emit(self.LISTEN, '')
                    break
                # msg = self.q2cloud.get()
                # if msg['cmd'] is 'upload_file':
                #     if msg['file_type'] is 'H264':
                #         self.h264_to_mp4(
                #             str(self.video_path / (msg['file_name'] + '.h264')),
                #             str(self.video_path / (msg['file_name'] + '.mp4')))
                #         self.upload_to_gdrive(self.video_path, msg)

                #     self.q2cloud.task_done()
        finally:
            # print('stopped')
            logging.info('cloud UDP stopped')
            # self.status.emit(self.STOP, '')


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    # config = json.load(open('./front_door.json'))

    cloud = Cloud(config)
    cloud.run()

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
