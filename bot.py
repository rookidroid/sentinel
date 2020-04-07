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
from telegram import Bot
import os
from email_util import Email
import logging


class MessageBot(Thread):
    def __init__(self, config, q2mbot):
        Thread.__init__(self)
        self.bot_name = config['bot']['bot_name']
        self.token = config['bot']['bot_token']
        self.bot = Bot(config['bot']['bot_token'])
        self.chat_id = config['bot']['chat_id']
        self.q2mbot = q2mbot

        self.email_handler = Email(config['email'])
        self.to_add = config['email']['to_add']

        self.emoji_robot = u'\U0001F916'

    def sendImage(self, msg):
        file = msg['path'] + msg['file_name'] + msg['extension']
        if msg['server'] == 'telegram':
            self.bot.sendPhoto(chat_id=self.chat_id,
                               photo=open(file, 'rb'),
                               caption=msg['file_name'])
        elif msg['server'] == 'email':
            print('send email')
            self.email_handler.send_email(
                self.to_add,
                '[Front Door] '+msg['date'] + ' ' + msg['time'],
                'Motion detected',
                msg_type='plain',
                path=file,
                file_name=msg['file_name'] + msg['extension'])
        logging.info('Send photo')
        os.remove(file)
        logging.info('Delete photo')

    def run(self):
        logging.info('MyBot thread started')
        self.bot.sendMessage(chat_id=self.chat_id,
                             text=self.emoji_robot + self.bot_name +
                             self.emoji_robot + ' is running...')

        while True:
            msg = self.q2mbot.get()
            print('get send_photo msg')
            if msg['cmd'] is 'send_photo':
                self.sendImage(msg)

            self.q2mbot.task_done()


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
