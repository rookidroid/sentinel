Help()
{
   # Display Help
   echo
   echo "Usages:"
   echo
   echo "Syntax: setup.sh --config=[/path/to/config.json]"
   echo "options:"
   echo "   --help	    Show the usages of the parameters"
   echo "   --config	Path to the config json file"
   echo
}

# CONFIG="./config.json"

for i in "$@"; do
  case $i in
    --help*)
      Help
      exit;;
    --config=*)
      CONFIG="${i#*=}"
      shift # past argument
      ;;
    --*)
      echo "Unknown option $1, Please check --help for usage"
      exit 1
      ;;
    *)
      echo "Please check --help for usage"
      exit 1
      ;;
  esac
done

echo "$CONFIG"

echo "create service files"
python3 create_services.py --config "$CONFIG"

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

