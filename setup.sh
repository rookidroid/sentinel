
echo "create service files"
python3 create_services.py

echo "copy service files to /lib/systemd/system"
service_dir=./service/
sudo cp "$service_dir"/* /lib/systemd/system/
sudo systemctl daemon-reload

echo "enable services"
# for entry in "$service_dir"/*
# do
#   echo "$entry"
# #   sudo systemctl enable "$entry"
# #   sudo systemctl start "$entry"
# done

service_names=`ls "$service_dir"/*.service`
for eachfile in $service_names
do
   echo $eachfile
done
