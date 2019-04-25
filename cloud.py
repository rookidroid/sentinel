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

from gdrive import GDrive
from threading import Thread
import logging


class Cloud(Thread):
    def __init__(self, config, q2cloud):
        Thread.__init__(self)
        self.q2cloud=q2cloud
        self.gdrive = GDrive()

    def run(self):
        logging.info('Camera thread started')
        while True:
            # retrieve data (blocking)
            msg = self.q2cloud.get()
            if msg['cmd'] is 'upload_file':
                #self.gdrive.upload(msg['arg'], mimetype, name, parents='root')

                self.q2cloud.task_done()