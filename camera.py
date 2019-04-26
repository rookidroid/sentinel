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
import picamera
import datetime
import queue
import logging


class Camera(Thread):
    def __init__(self, config, q2camera, q2mbot, q2cloud):
        Thread.__init__(self)
        self.motion2camera = q2camera
        self.camera2mbot = q2mbot
        self.q2cloud = q2cloud
        self.camera = picamera.PiCamera(resolution=config['resolution'])
        self.max_photo_count = config['max_photo_count']
        self.max_video_count = 2
        self.period = config['period']
        self.video_length = 30

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
                self.camera2mbot.put({'cmd': 'send_photo', 'arg': filename})

                try:
                    msg = self.motion2camera.get(block=True, timeout=period)
                except queue.Empty:
                    # Handle empty queue here
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
        ready_filename = './videos/video0_' + datetime_str + '.h264'

        def take_photo_during_recording(video_filename, photo_filename):
            for photo_idx in range(0, int(self.video_length/self.period)):
                try:
                    msg = self.motion2camera.get(block=True,
                                                timeout=self.period)
                except queue.Empty:
                    self.camera.capture(photo_filename, use_video_port=True)
                    self.camera2mbot.put({'cmd': 'send_photo', 'arg': photo_filename})
                    pass
                else:
                    if msg['cmd'] is 'stop':
                        self.camera.stop_recording()
                        self.motion2camera.task_done()
                        self.q2cloud.put({'cmd':'upload_file', 'file_type':'H264', 'file_name':video_filename})
                        #self.camera2mbot.put({'cmd': 'send_image', 'arg': filename})
                        # process video
                        logging.info('Stop recording')
                        break
                    else:
                        self.motion2camera.task_done()
                        logging.warning('Wrong command, continue recording')
                    pass

        self.camera.start_recording(ready_filename)
        take_photo_during_recording(ready_filename, './photos/image0_' + datetime_str + '.jpg')
        
        if count > 1:

            for video_idx in range(1, count):
                file_name = './videos/video'+ str(video_idx)+'_' + datetime_str + '.h264'

                self.camera.split_recording(file_name)
                self.q2cloud.put({'cmd':'upload_file', 'file_type':'H264', 'file_name':ready_filename})
                ready_filename=file_name

                take_photo_during_recording(ready_filename, './photos/image'+ str(video_idx)+'_' + datetime_str + '.jpg')

            self.camera.stop_recording()
            self.q2cloud.put({'cmd':'upload_file', 'file_type':'H264', 'file_name':ready_filename})
            # process video

        else:
            self.camera.stop_recording()
            self.q2cloud.put({'cmd':'upload_file', 'file_type':'H264', 'file_name':ready_filename})

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
                self.take_video()
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
