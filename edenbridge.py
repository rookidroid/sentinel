# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
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
'''

from queue import Queue
from motion import Motion
from bot import MyBot
from camera import Camera
import json


def get_config():
    with open("config.json", "r") as read_file:
        return json.load(read_file)


def main():
    config = get_config()
    motion2bot_queue = Queue()
    motion2camera = Queue()
    camera2bot = Queue()

    motion = Motion(config['motion'], motion2camera)
    my_bot = MyBot(config['bot'], camera2bot)
    camera =  Camera(config['camera'], motion2camera, camera2bot)

    motion.start()
    my_bot.start()
    camera.start()


if __name__ == '__main__':
    main()
'''
    Z. Peng

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