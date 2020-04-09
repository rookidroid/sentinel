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
from telegram import Bot
import os
from email_util import send_email
import logging

logging.basicConfig(
    filename='info.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class MessageBot(Thread):
    def __init__(self, config, q2mbot):
        Thread.__init__(self)
        self.q2mbot = q2mbot

        self.location = config['name']
        self.photo_path = Path(config['photo_path'])

        # telegram bot
        self.bot_config = config['bot']
        self.bot_name = self.bot_config['bot_name']
        self.token = self.bot_config['bot_token']
        self.chat_id = self.bot_config['chat_id']

        self.bot = Bot(self.token)

        # email
        self.email_config = config['email']
        self.mail_server = self.email_config['mail_server']
        self.mail_body = self.email_config['mail_body']
        self.attachement = dict(path=config['photo_path'],
                                file_name='')

        self.emoji_robot = u'\U0001F916'

    def sendImage(self, msg):
        file = self.photo_path / (msg['file_name'] + msg['extension'])
        if msg['server'] == 'telegram':
            self.bot.sendPhoto(chat_id=self.chat_id,
                               photo=open(file, 'rb'),
                               caption='A photo has been taken from your [' +
                               self.location +
                               '] at '+msg['date'] + ' '+msg['time'],
                               timeout=100)

        elif msg['server'] == 'email':
            self.mail_body['subject'] = '[Front Door] ' + \
                msg['date'] + ' ' + msg['time']
            self.mail_body['message'] = 'A photo has been taken from your [' +\
                self.location +\
                '] at '+msg['date'] + ' '+msg['time']

            self.attachement['file_name'] = msg['file_name'] + msg['extension']

            send_email(self.mail_server, self.mail_body, self.attachement)

            self.bot.sendMessage(chat_id=self.chat_id,
                                 text='"'+msg['file_name'] +
                                      msg['extension'] +
                                 '" has been sent to your email.')

        logging.info('Send photo')
        os.remove(file)
        logging.info('Delete photo')

    def run(self):
        logging.info('MyBot thread started')
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text='Hello! ' + self.emoji_robot + self.bot_name +
            self.emoji_robot + ' [' + self.location+'] is at your service.')

        while True:
            msg = self.q2mbot.get()
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
