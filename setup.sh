sudo cp ./service/* /lib/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable message_bot
sudo systemctl enable camera