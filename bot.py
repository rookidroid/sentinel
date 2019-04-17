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

from telegram import Bot
import datetime

def bot(config, input_queue):
    bot = Bot(config['bot_token'])
    chat_id = config['chat_id']
    
#    def bop(bot, update):
#        #url = get_url()
#        chat_id = update.message.chat_id
#        print(chat_id)
#        #bot.send_photo(chat_id=chat_id, photo=url)
#    
#    updater = Updater('')
#    dp = updater.dispatcher
#    dp.add_handler(CommandHandler('bop',bop))
#
#    updater.start_polling()
#    updater.idle()

    while True:
        # retrieve data (blocking)
        data = input_queue.get()

        # do something with the data
        currentDT = str(datetime.datetime.now())
        bot.sendMessage(chat_id=chat_id, text=data + ' at ' + currentDT, parse_mode='HTML')

        # indicate data has been consumed
        input_queue.task_done()
        
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