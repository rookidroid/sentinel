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

from queue import Queue
from bot import MessageBot
from camera import Camera
from cloud import Cloud
import argparse
import json
from telegram.ext import Updater, CallbackContext
from telegram.ext import InlineQueryHandler, CommandHandler
import time


def main():
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    config = json.load(open(args["conf"]))

    token = config['bot']['bot_token']
    chat_id = config['bot']['chat_id']
    q2camera = Queue()
    q2mbot = Queue()
    q2cloud = Queue()

    def hello(update, context):
        user_id = update.message.chat_id
        if user_id == chat_id:
            context.bot.sendMessage(chat_id=user_id, text='Hello!')

    def take_photo(update, context):
        user_id = update.message.chat_id
        if user_id == chat_id:
            q2camera.put({'cmd': 'take_photo', 'count': 1})

    def take_video(update, context):
        user_id = update.message.chat_id
        if user_id == chat_id:
            q2camera.put({'cmd': 'take_video', 'count': 1})

    my_bot = MessageBot(config, q2mbot)
    camera = Camera(config, q2camera, q2mbot, q2cloud)
    cloud = Cloud(config, q2cloud)

    my_bot.start()
    camera.start()
    cloud.start()

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('photo', take_photo))
    dp.add_handler(CommandHandler('video', take_video))

    # updater.start_polling()
    updater.idle()


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
