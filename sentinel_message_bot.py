#!/usr/bin/env python3
"""
    Project Sentinel
    Copyright (C) 2019 - PRESENT  rookidroid.com

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

import os
import asyncio
from pathlib import Path
import argparse
import json
import socket
import logging

from telegram import Bot


pwd = os.path.dirname(os.path.realpath(__file__))
log_folder = os.path.join(pwd, "log")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(
    filename=os.path.join(log_folder, "message_bot.log"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
)


class MessageBot:
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, config):
        self.location = config["name"]
        self.photo_path = Path(config["photo_path"])

        # telegram bot
        self.bot_config = config["bot"]
        self.bot_name = self.bot_config["bot_name"]
        self.token = self.bot_config["bot_token"]
        self.chat_id = self.bot_config["chat_id"]

        self.bot = Bot(self.token)

        self.emoji_robot = "\U0001F916"

        self.ip = "127.0.0.1"
        self.port = self.bot_config["listen_port"]
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(1)

    async def sendImage(self, msg):
        file = self.photo_path / (msg["file_name"] + msg["extension"])
        if msg["server"] == "telegram":
            async with self.bot:
                await self.bot.sendPhoto(
                    chat_id=self.chat_id,
                    photo=open(file, "rb"),
                    caption="A photo has been taken from your ["
                    + self.location
                    + "] at "
                    + msg["date"]
                    + " "
                    + msg["time"],
                )

        logging.info("Send photo")
        os.remove(file)
        logging.info("Delete photo")

    async def sendMsg(self, msg):
        async with self.bot:
            await self.bot.sendMessage(
                chat_id=self.chat_id,
                text="Motion detected in ["
                + self.location
                + "] at "
                + msg["date"]
                + " "
                + msg["time"],
            )

    async def run(self):
        logging.info("MyBot thread started")
        async with self.bot:
            await self.bot.sendMessage(
                chat_id=self.chat_id,
                text="Hello! "
                + self.emoji_robot
                + self.bot_name
                + self.emoji_robot
                + " ["
                + self.location
                + "] is at your service.",
            )

        try:
            self.udp_socket.bind((self.ip, self.port))
        except OSError as err:
            logging.error(err)
        else:
            while True:
                try:
                    data, _ = self.udp_socket.recvfrom(4096)
                except socket.timeout as t_out:
                    logging.info(t_out)
                else:
                    if data:
                        try:
                            msg = json.loads(data.decode())
                            if msg["cmd"] == "send_photo":
                                await self.sendImage(msg)
                            elif msg["cmd"] == "send_msg":
                                await self.sendMsg(msg)
                        except (
                            Exception  # pylint: disable=broad-exception-caught
                        ) as exp:
                            logging.error(exp)
                    else:
                        continue
        finally:
            logging.info("bot UDP stopped")


async def main():
    """Main function"""
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c", "--conf", required=True, help="path to the JSON configuration file"
    )
    args = vars(ap.parse_args())
    with open(args["conf"], "r", encoding="utf-8") as read_file:
        config = json.load(read_file)

    my_bot = MessageBot(config)
    await my_bot.run()


if __name__ == "__main__":
    asyncio.run(main())
