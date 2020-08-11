# Edenbridge

A DIY smart camera based on Raspberry Pi, Telegram bot and Google Drive.

## Hardware

- Raspberry Pi Zero W or Raspberry Pi
- Camera module

## Usage

- Shell
`chmod +x edenbridge.sh`
`./edenbridge.sh`

- Systemd
`chmod +x setup.sh`
`sudo setup.sh`

## Function

When the motion is detected by the camera

- A series of photos will be send to you through Telegram Bot
- A video clip will be recorded and uploaded to Google Drive

In additional, you can ask the camera to take a photo or a video anytime through Telegram
