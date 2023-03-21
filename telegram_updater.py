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

import argparse
import json

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import time
import socket
import logging

logging.basicConfig(
    filename='/home/pi/sentinel/telegram.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR)


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    # config = json.load(open('./garage.json'))

    token = config['bot']['bot_token']
    chat_id = config['bot']['chat_id']

    camera_port = config['camera']['listen_port']
    bot_port = config['bot']['listen_port']
    cloud_port = config['cloud']['listen_port']

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_udp(msg, port):
        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = json.dumps(msg)
        udp_socket.sendto(payload.encode(), ('127.0.0.1', port))

    def echo(update, context):
        user_id = update.effective_chat.id
        if user_id == chat_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=update.message.text)

    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == chat_id:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == chat_id:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

    async def take_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == chat_id:
            send_udp({'cmd': 'take_photo', 'count': 1}, camera_port)

    async def take_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == chat_id:
            send_udp({'cmd': 'take_video', 'count': 1}, camera_port)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('hello', hello))
    application.add_handler(CommandHandler('photo', take_photo))
    application.add_handler(CommandHandler('video', take_video))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


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
