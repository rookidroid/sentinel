
echo "create service files"
python3 create_services.py

echo "copy service files to /lib/systemd/system"
service_dir=./service/
sudo cp "$service_dir"/* /lib/systemd/system/
sudo systemctl daemon-reload

echo "enable services"
cd "$service_dir"
service_names=`ls`
for eachfile in $service_names
do
  echo "$eachfile"
  sudo systemctl enable "$eachfile"
  sudo systemctl start "$eachfile"
done
cd ..

