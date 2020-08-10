sudo cp ./service/* /lib/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable message_bot
sudo systemctl enable camera
sudo systemctl enable telegram_updater
sudo systemctl enable cloud

sudo systemctl start message_bot
sudo systemctl start camera
sudo systemctl start telegram_updater
sudo systemctl start cloud