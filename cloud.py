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

from pathlib import Path
from threading import Thread
from subprocess import call, Popen
import os
import logging


class Cloud(Thread):
    def __init__(self, config, q2cloud):
        Thread.__init__(self)
        self.q2cloud = q2cloud

        self.video_path = Path(config['video_path'])
        self.photo_path = Path(config['photo_path'])

        self.target_folder = config['cloud']['folder']
        self.rclone_remote = config['cloud']['rclone_remote']

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
        while True:
            msg = self.q2cloud.get()
            if msg['cmd'] is 'upload_file':
                if msg['file_type'] is 'H264':
                    self.h264_to_mp4(
                        str(self.video_path / (msg['file_name'] + '.h264')),
                        str(self.video_path / (msg['file_name'] + '.mp4')))
                    self.upload_to_gdrive(self.video_path, msg)

                self.q2cloud.task_done()


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
