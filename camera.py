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
from pathlib import Path
import picamera
import datetime
import queue
import copy
import logging


class Camera(Thread):
    def __init__(self, config, q2camera, q2mbot, q2cloud):
        Thread.__init__(self)
        self.cwd = Path().absolute()
        self.motion2camera = q2camera
        self.q2mbot = q2mbot
        self.q2cloud = q2cloud
        self.camera = picamera.PiCamera(resolution=config['resolution'])
        self.max_photo_count = config['max_photo_count']
        self.max_video_count = 10
        self.period = config['period']
        self.video_length = 30
        self.video_path = str(self.cwd) + '/videos/'
        self.photo_path = str(self.cwd) + '/photos/'

        self.cmd_upload_h264 = {
            'cmd': 'upload_file',
            'path': self.video_path,
            'file_type': 'H264',
            'file_name': '',
            'extension': '.h264',
            'date': '',
            'time': ''
        }

        self.cmd_send_jpg = {
            'cmd': 'send_photo',
            'path': self.photo_path,
            'file_type': 'JPG',
            'file_name': '',
            'extension': '.jpg',
            'date': '',
            'time': ''
        }

    def take_photo(self, counts, period):

        if counts == 0 or counts > self.max_photo_count:
            counts = self.max_photo_count

        for photo_idx in range(0, counts):
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.datetime.now().strftime('%H-%M-%S')

            self.cmd_send_jpg['date'] = date_str
            self.cmd_send_jpg['time'] = time_str
            self.cmd_send_jpg['file_name'] = 'photo' + str(
                photo_idx) + '_' + date_str + '_' + time_str

            self.camera.capture(self.cmd_send_jpg['path'] +
                                self.cmd_send_jpg['file_name'] +
                                self.cmd_send_jpg['extension'])
            self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))

            try:
                msg = self.motion2camera.get(block=True, timeout=period)
            except queue.Empty:
                pass
            else:
                if msg['cmd'] is 'stop':
                    self.motion2camera.task_done()
                    logging.info('Stop capturing')
                    break
                else:
                    self.motion2camera.task_done()
                    logging.warning('Wrong command, continue capturing')
                pass

    def take_video(self, count):
        def take_photo_during_recording(video_idx, date, time):
            for photo_idx in range(0, int(self.video_length / self.period)):
                try:
                    msg = self.motion2camera.get(block=True,
                                                 timeout=self.period)
                except queue.Empty:
                    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                    time_str = datetime.datetime.now().strftime('%H-%M-%S')
                    self.cmd_send_jpg['file_name'] = 'photo' + str(
                        int(1 + photo_idx +
                            video_idx * int(self.video_length / self.period))
                    ) + '_' + date_str + '_' + time_str
                    self.cmd_send_jpg['date'] = date_str
                    self.cmd_send_jpg['time'] = time_str
                    self.camera.capture(self.cmd_send_jpg['path'] +
                                        self.cmd_send_jpg['file_name'] +
                                        self.cmd_send_jpg['extension'],
                                        use_video_port=True)
                    self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))
                    pass
                else:
                    if msg['cmd'] is 'stop':
                        self.camera.stop_recording()
                        self.motion2camera.task_done()

                        self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))

                        logging.info('Stop recording')
                        break
                    else:
                        self.motion2camera.task_done()
                        logging.warning('Wrong command, continue recording')
                    pass

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        self.cmd_upload_h264['file_name'] = 'video' + str(
            0) + '_' + date_str + '_' + time_str
        self.cmd_upload_h264['date'] = date_str
        self.cmd_upload_h264['time'] = time_str

        self.cmd_send_jpg['file_name'] = 'photo' + str(
            0) + '_' + date_str + '_' + time_str
        self.cmd_send_jpg['date'] = date_str
        self.cmd_send_jpg['time'] = time_str

        self.camera.start_recording(self.cmd_upload_h264['path'] +
                                    self.cmd_upload_h264['file_name'] +
                                    self.cmd_upload_h264['extension'])
        self.camera.capture(self.cmd_send_jpg['path'] +
                            self.cmd_send_jpg['file_name'] +
                            self.cmd_send_jpg['extension'],
                            use_video_port=True)
        self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))

        take_photo_during_recording(0, date_str, time_str)

        if count > 1:

            for video_idx in range(1, count):
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                time_str = datetime.datetime.now().strftime('%H-%M-%S')

                temp_cmd = copy.deepcopy(self.cmd_upload_h264)

                self.cmd_upload_h264['file_name'] = 'video' + str(
                    video_idx) + '_' + date_str + '_' + time_str
                self.cmd_upload_h264['date'] = date_str
                self.cmd_upload_h264['time'] = time_str
                self.camera.split_recording(self.cmd_upload_h264['path'] +
                                            self.cmd_upload_h264['file_name'] +
                                            self.cmd_upload_h264['extension'])

                self.q2cloud.put(temp_cmd)

                take_photo_during_recording(video_idx, date_str, time_str)

            self.camera.stop_recording()
            self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))

        else:
            self.camera.stop_recording()
            self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))

    def run(self):
        logging.info('Camera thread started')
        while True:
            # retrieve data (blocking)
            msg = self.motion2camera.get()
            if msg['cmd'] is 'take_photo':
                self.motion2camera.task_done()
                self.take_photo(msg['count'], self.period)
                logging.info('Start to capture photos')
            elif msg['cmd'] is 'take_video':
                self.motion2camera.task_done()
                self.take_video(msg['count'])
                logging.info('Start to record videos')
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
