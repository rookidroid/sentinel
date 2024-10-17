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

import copy
import logging

import argparse
import json
import socket

from pathlib import Path
import datetime

from picamera2 import Picamera2, Preview


pwd = os.path.dirname(os.path.realpath(__file__))
log_folder = os.path.join(pwd, "log")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(
    filename=os.path.join(log_folder, "camera.log"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
)


class Camera:
    """
    A class to manage the camera module.

    ...

    Methods
    -------
    take_photo(counts):
        Takes a specified number of photos.
    take_video(init_photo=False):
        Records a video.
    run():
        Starts the camera module.
    message_handling_loop():
        Handles incoming messages.
    send_bot(msg):
        Sends a message to the bot.
    send_cloud(msg):
        Sends a message to the cloud.
    """

    def __init__(self, config):
        """
        Initializes the camera module.

        Parameters
        ----------
        config : dict
            The configuration dictionary.
        """

        self.video_path = Path(config["video_path"])
        self.photo_path = Path(config["photo_path"])

        self.camera_config = config["camera"]

        self.ip = "127.0.0.1"
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(3)

        self.bot_port = config["bot"]["listen_port"]
        # self.cloud_port = config["cloud"]["listen_port"]

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start_preview(Preview.NULL)

        try:
            os.makedirs(self.video_path)
        except FileExistsError:
            pass

        try:
            os.makedirs(self.photo_path)
        except FileExistsError:
            pass

        self.cmd_upload_h264 = {
            "cmd": "upload_file",
            "file_type": "H264",
            "file_name": "",
            "extension": ".mp4",
            "date": "",
            "time": "",
        }

        self.cmd_send_jpg = {
            "cmd": "send_photo",
            "file_type": "JPG",
            "file_name": "",
            "extension": ".jpg",
            "date": "",
            "time": "",
            "server": "",
        }

    def take_photo(self, counts):
        """Takes a specified number of photos.

        Parameters
        ----------
        counts : int
            The number of photos to take.
        """
        if counts == 0 or counts > self.camera_config["max_photo_count"]:
            counts = self.camera_config["max_photo_count"]

        for photo_idx in range(0, counts):
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.datetime.now().strftime("%H-%M-%S")

            self.cmd_send_jpg["date"] = date_str
            self.cmd_send_jpg["time"] = time_str
            self.cmd_send_jpg["file_name"] = (
                date_str + "_" + time_str + "_" + "photo" + str(photo_idx)
            )
            self.cmd_send_jpg["server"] = "telegram"

            self.picam2.start_and_capture_file(
                str(
                    self.photo_path
                    / (self.cmd_send_jpg["file_name"] + self.cmd_send_jpg["extension"])
                ),
                delay=1,
                show_preview=False,
            )

            self.send_bot(copy.deepcopy(self.cmd_send_jpg))

    def take_video(self):
        """Records a video.

        Parameters
        ----------
        init_photo : bool, optional
            Whether to take a photo before recording the video, by default False.
        """
        self.take_photo(1)

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.datetime.now().strftime("%H-%M-%S")
        self.cmd_upload_h264["file_name"] = time_str + "_" + "video"
        self.cmd_upload_h264["date"] = date_str
        self.cmd_upload_h264["time"] = time_str

        self.picam2.start_and_record_video(
            str(
                self.video_path
                / (
                    self.cmd_upload_h264["file_name"]
                    + self.cmd_upload_h264["extension"]
                )
            ),
            duration=self.camera_config["video_length"],
        )

    def run(self):
        """Starts the camera module."""
        logging.info("Camera thread started")
        try:
            self.udp_socket.bind((self.ip, self.camera_config["listen_port"]))
        except OSError as err:
            logging.error(err)
        else:
            self.message_handling_loop()
        finally:
            logging.info("camera UDP stopped")

    def message_handling_loop(self):
        """Handles incoming messages."""
        while True:
            try:
                data, _ = self.udp_socket.recvfrom(4096)
            except socket.timeout as t_out:
                logging.info(t_out)
            else:
                if data:
                    try:
                        msg = json.loads(data.decode())
                        # logging.info(data.decode())
                        if msg["cmd"] == "take_photo":
                            self.take_photo(msg["count"])
                            logging.info("Start to capture photos")
                        elif msg["cmd"] == "take_video":
                            self.take_video()
                            logging.info("Start to record videos")
                    except Exception as exp:  # pylint: disable=broad-exception-caught
                        logging.error(exp)
                else:
                    continue

    def send_bot(self, msg):
        """Sends a message to the bot.

        Parameters
        ----------
        msg : dict
            The message to send.
        """
        payload = json.dumps(msg)
        self.udp_socket.sendto(payload.encode(), ("127.0.0.1", self.bot_port))

    # def send_cloud(self, msg):
    #     """Sends a message to the cloud.

    #     Parameters
    #     ----------
    #     msg : dict
    #         The message to send.
    #     """
    #     payload = json.dumps(msg)
    #     self.udp_socket.sendto(payload.encode(), ("127.0.0.1", self.cloud_port))


def main():
    """Main function"""
    # argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c", "--conf", required=True, help="path to the JSON configuration file"
    )
    args = vars(ap.parse_args())
    with open(args["conf"], "r", encoding="utf-8") as read_file:
        config = json.load(read_file)

    camera = Camera(config)
    camera.run()


if __name__ == "__main__":
    main()
