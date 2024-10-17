# Project Sentinel

Project Sentinel is a Raspberry Pi-based motion detection system designed to enhance home security. It utilizes a motion sensor to detect movement, and when triggered, it captures photos of the activity. These photos are automatically sent to the user's smartphone via a Telegram bot, allowing for real-time monitoring from anywhere. The entire system is housed in a custom 3D-printed enclosure, making it compact and easily customizable.

## Hardware

- Raspberry Pi Zero W, Raspberry Pi Zero 2 W or Raspberry Pi
- Camera module

## Installation

### 1. Install Required Packages

```bash
sudo apt install git python3-pip
sudo apt install python3-picamera2 --no-install-recommends
```

### 2. Install Telegram Bot Python API

```bash
pip3 install python-telegram-bot
```

> For `externally-managed-environment` error, you can enable the installation of python package "system-wide" with a potential risk of breaking your system.
>
> ```bash
> python3 -m pip config set global.break-system-packages true
> ```

### 3. Clone Sentinel Package

```bash
git clone https://github.com/rookidroid/sentinel.git
cd sentinel
```

### 4. Create Telegram Bot

Follow this [instruction](https://core.telegram.org/bots/tutorial) to create a Telegram Bot. You will need the **name** and **token** of the new bot.

You will also need to find your Telegram **Chat ID**.

### 5. Configuration

Edit the `config.json`. Update `bot_name`, `bot_token` and `chat_id` with the ones obtianed from step 4.

### 6. Setup Services

```bash
chmod +x setup.sh
./setup.sh --config=./config.json
```

## Usage

When the motion is detected by the camera

- A series of photos will be send to you through Telegram Bot
- A video clip will be recorded and uploaded to Google Drive

In additional, you can ask the camera to take a photo or a video anytime through Telegram


