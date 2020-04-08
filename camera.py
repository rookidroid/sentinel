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

from threading import Thread
from pathlib import Path
import os
import picamera
from picamera.array import PiRGBArray
import datetime
import queue
import copy
import logging
import numpy as np

import imutils
import cv2
import time


class Camera(Thread):
    def __init__(self, config, q2camera, q2mbot, q2cloud):
        Thread.__init__(self)
        self.video_path = Path(config['video_path'])
        self.photo_path = Path(config['photo_path'])

        self.camera_config = config['camera']
        # self.cwd = Path().absolute()
        self.q2camera = q2camera
        self.q2mbot = q2mbot
        self.q2cloud = q2cloud

        self.max_photo_count = self.camera_config['max_photo_count']
        self.period = self.camera_config['period']
        self.video_length = self.camera_config['video_length']

        self.det_resolution = self.camera_config['detection_resolution']
        self.rec_resolution = self.camera_config['record_resolution']

        self.delta_thresh = self.camera_config['delta_thresh']
        self.min_area = self.camera_config['min_area']
        self.motion_frame_counter = 0

        # initialize the camera and grab a reference to the raw camera capture
        # camera.resolution = tuple(conf["resolution"])
        # camera.framerate = conf["fps"]
        self.camera = picamera.PiCamera(resolution=self.det_resolution)
        self.raw_capture = PiRGBArray(
            self.camera,
            size=self.det_resolution)

        # allow the camera to warmup, then initialize the average frame, last
        # uploaded timestamp, and frame motion counter
        logging.info('Camera warming up')
        time.sleep(self.camera_config["camera_warmup_time"])
        self.avg_capture = None

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
            'time': '',
            'server': ''
        }

    def take_photo(self, counts):
        self.camera.resolution = self.rec_resolution

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

            self.camera.capture(str(
                self.photo_path /
                (self.cmd_send_jpg['file_name'] + self.cmd_send_jpg['extension'])))

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
            self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))

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
            self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))

        self.camera.stop_recording()
        self.q2cloud.put(copy.deepcopy(self.cmd_upload_h264))

    def motion_detection(self):
        self.camera.resolution = self.det_resolution
        self.avg_capture = None
        self.motion_frame_counter = 0
        is_occupied = False

        # capture frames from the camera
        for frm in self.camera.capture_continuous(
                self.raw_capture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            raw_frame = frm.array

            # clear the stream in preparation for the next frame
            self.raw_capture.truncate(0)

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(raw_frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the average frame is None, initialize it
            if self.avg_capture is None:
                # if self.motion_frame_counter < 2:
                #     self.motion_frame_counter += 1
                # print("[INFO] starting background model...")
                self.avg_capture = gray.copy().astype("float")
                # self.raw_capture.truncate(0)
                continue

            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(gray, self.avg_capture, 0.5)
            frame_delta = cv2.absdiff(
                gray, cv2.convertScaleAbs(self.avg_capture))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frame_delta, self.delta_thresh, 255,
                                   cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            # loop over the contours
            for contr in contours:
                # if the contour is too small, ignore it
                if cv2.contourArea(contr) < self.min_area:
                    continue

                scale_factor = self.det_resolution[0]/500
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                time_str = datetime.datetime.now().strftime('%H-%M-%S')
                # draw box and timestamp on frame
                (x, y, w, h) = cv2.boundingRect(contr)
                cv2.rectangle(raw_frame,
                              (int(scale_factor*x),
                               int(scale_factor*y)),
                              (int(scale_factor*(x + w)),
                               int(scale_factor*(y + h))),
                              (0, 255, 0),
                              1)
                cv2.putText(raw_frame, 'Front Door', (10, 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                cv2.putText(raw_frame, date_str + '_' + time_str,
                            (10, raw_frame.shape[0] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 1)

                self.cmd_send_jpg['date'] = date_str
                self.cmd_send_jpg['time'] = time_str
                self.cmd_send_jpg['file_name'] = date_str + '_' + time_str
                self.cmd_send_jpg['server'] = 'telegram'

                cv2.imwrite(self.cmd_send_jpg['path'] +
                            self.cmd_send_jpg['file_name'] +
                            self.cmd_send_jpg['extension'],
                            raw_frame)
                self.q2mbot.put(copy.deepcopy(self.cmd_send_jpg))

                is_occupied = True
                return is_occupied

            self.motion_frame_counter += 1
            if self.motion_frame_counter >= 5:
                return is_occupied

    def run(self):
        logging.info('Camera thread started')
        while True:
            status = self.motion_detection()
            # print(status)
            if status:
                self.take_video(init_photo=False)
            else:
                # retrieve data (blocking)
                try:
                    msg = self.q2camera.get(block=True, timeout=3)
                    if msg['cmd'] is 'take_photo':
                        self.q2camera.task_done()
                        self.take_photo(msg['count'])
                        logging.info('Start to capture photos')
                    elif msg['cmd'] is 'take_video':
                        self.q2camera.task_done()
                        self.take_video(init_photo=True)
                        logging.info('Start to record videos')
                    else:
                        self.q2camera.task_done()
                except queue.Empty:
                    pass


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
