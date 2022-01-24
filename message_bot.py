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
from telegram import Bot
import os
from email_util import send_email
import argparse
import json
import socket
import logging

logging.basicConfig(
    filename='/home/pi/sentinel/message_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class MessageBot():
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, config):
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

        self.ip = '127.0.0.1'
        self.port = self.bot_config['listen_port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(1)
        self.signal = self.SIG_NORMAL

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

        logging.info('Send photo')
        os.remove(file)
        logging.info('Delete photo')

    def sendMsg(self, msg):
        self.bot.sendMessage(chat_id=self.chat_id,
                             text='Motion detected in [' +
                             self.location +
                             '] at '+msg['date'] + ' '+msg['time'])

    def run(self):
        logging.info('MyBot thread started')
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text='Hello! ' + self.emoji_robot + self.bot_name +
            self.emoji_robot + ' [' + self.location+'] is at your service.')

        try:
            self.udp_socket.bind((self.ip, self.port))
        except OSError as err:
            logging.error(err)
        else:
            while True:
                if self.signal == self.SIG_NORMAL:
                    try:
                        data, addr = self.udp_socket.recvfrom(4096)
                    except socket.timeout as t_out:
                        pass
                    else:
                        if data:
                            try:
                                msg = json.loads(data.decode())
                                if msg['cmd'] == 'send_photo':
                                    self.sendImage(msg)
                                elif msg['cmd'] == 'send_msg':
                                    self.sendMsg(msg)
                            except Exception:
                                logging.error(Exception)
                        else:
                            break
                elif self.signal == self.SIG_STOP:
                    self.signal = self.SIG_NORMAL
                    self.udp_socket.close()
                    break
        finally:
            logging.info('bot UDP stopped')


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    my_bot = MessageBot(config)
    my_bot.run()


if __name__ == '__main__':
    main()


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
