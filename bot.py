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

from threading import Thread
from telegram import Bot
import datetime
import requests
import os
import logging


class MessageBot(Thread):
    def __init__(self, config, camera2mbot):
        Thread.__init__(self)
        self.bot_name = config['bot_name']
        self.token = config['bot_token']
        self.bot = Bot(config['bot_token'])
        self.chat_id = config['chat_id']
        self.camera2mbot = camera2mbot

        self.emoji_robot = u'\U0001F916'

    def sendImage(self, filename):
        self.bot.sendPhoto(chat_id=self.chat_id, photo=open(filename, 'rb'))
        logging.info('Send photo')
        os.remove(filename)
        logging.info('Delete photo')

    def run(self):
        logging.info('MyBot thread started')
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text=self.emoji_robot + self.bot_name + self.emoji_robot +
            ' is running...')

        while True:
            # retrieve data (blocking)
            data = self.camera2mbot.get()

            # do something with the data
            currentDT = str(datetime.datetime.now())
            # self.bot.sendMessage(
            #     chat_id=self.chat_id, text=data + ' at ' + currentDT)
            self.sendImage(data)

            # indicate data has been consumed
            self.camera2mbot.task_done()

# class CommandBot(Thread):
#     def __init__(self, config, camera2mbot):
#         Thread.__init__(self)

#     def run(self):
#         while True:


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