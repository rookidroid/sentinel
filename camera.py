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

    def take_photo(self, counts, period):
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        try:
            for frame_idx, filename in enumerate(
                    self.camera.capture_continuous(
                        './photos/photo{counter:d}' + '_' + datetime_str +
                        '.jpg')):

                if (counts > 0 and frame_idx >= counts) or (
                        frame_idx >= self.max_photo_count):
                    logging.warning('Reach to maximum number of photos')
                    break

                logging.info('Capture ' + filename)
                self.q2mbot.put({'cmd': 'send_photo', 'arg': filename})

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
        finally:
            pass

    def take_video(self, count):
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        def take_photo_during_recording(video_idx, date, time):
            for photo_idx in range(0, int(self.video_length / self.period)):
                try:
                    msg = self.motion2camera.get(block=True,
                                                 timeout=self.period)
                except queue.Empty:
                    photo_filename = self.photo_path + 'photo' + str(
                        int(1 + photo_idx +
                            video_idx * int(self.video_length / self.period))
                    ) + '_' + datetime.datetime.now().strftime(
                        '%Y-%m-%d_%H-%M-%S') + '.jpg'
                    self.camera.capture(photo_filename, use_video_port=True)
                    self.q2mbot.put({
                        'cmd': 'send_photo',
                        'arg': photo_filename
                    })
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
        video_ready_name = self.video_path + 'video' + str(
            0) + '_' + date_str + '_' + time_str + '.h264'
        photo_ready_name = './photos/photo0_' + datetime_str + '.jpg'

        self.camera.start_recording(video_ready_name)
        self.camera.capture(photo_ready_name, use_video_port=True)
        self.q2mbot.put({'cmd': 'send_photo', 'arg': photo_ready_name})

        take_photo_during_recording(0, date_str, time_str)

        if count > 1:

            for video_idx in range(1, count):
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                time_str = datetime.datetime.now().strftime('%H-%M-%S')
                video_name = self.video_path + 'video' + str(
                    video_idx) + '_' + date_str + '_' + time_str + '.h264'

                self.camera.split_recording(video_name)
                self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))

                self.cmd_upload_h264['file_name'] = 'video' + str(
                    video_idx) + '_' + date_str + '_' + time_str
                self.cmd_upload_h264['date'] = date_str
                self.cmd_upload_h264['time'] = time_str
                take_photo_during_recording(video_idx, date_str, time_str)

            self.camera.stop_recording()
            self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))
            # process video

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
