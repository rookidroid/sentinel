
python3 create_services.py

service_dir=./service/

sudo cp "$service_dir"/* /lib/systemd/system/
sudo systemctl daemon-reload

for entry in "$service_dir"/*
do
  echo "$entry"
  sudo systemctl enable "$entry"
  sudo systemctl start "$entry"
done
