#!/bin/sh

python3 message_bot.py -c front_door.json &
python3 camera.py -c front_door.json &
python3 telegram_updater.py -c front_door.json &
python3 cloud.py -c front_door.json &