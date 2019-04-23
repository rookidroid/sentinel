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

from queue import Queue
from motion import Motion
from bot import MessageBot
from camera import Camera
import json
from telegram.ext import Updater, InlineQueryHandler, CommandHandler


def get_config():
    with open("config.json", "r") as read_file:
        return json.load(read_file)


def main():
    config = get_config()
    token = config['bot']['bot_token']
    chat_id = config['bot']['chat_id']
    q2camera = Queue()
    q2mbot = Queue()

    def hello(bot, update):
        user_id = update.message.chat_id
        if user_id == chat_id:
            bot.sendMessage(chat_id=user_id, text='Hello!')

    def get_photo(bot, update):
        user_id = update.message.chat_id
        if user_id == chat_id:
            q2camera.put({'cmd': 'capture_jpg', 'arg': 1})

    motion = Motion(config['motion'], q2camera)
    my_bot = MessageBot(config['bot'], q2mbot)
    camera = Camera(config['camera'], q2camera, q2mbot)

    motion.start()
    my_bot.start()
    camera.start()

    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('photo', get_photo))

    updater.start_polling()
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
