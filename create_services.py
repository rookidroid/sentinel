import getpass
import os, shutil
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True, help="Path to the config json file")
args, unknown = ap.parse_known_args()

config_file = os.path.realpath(args.config)

pwd = os.path.dirname(os.path.realpath(__file__))
service_folder = "./service"
user = getpass.getuser()

service_files = []
for dirpath, dirnames, files in os.walk("./"):
    for name in files:
        if name.lower().startswith("sentinel_"):
            service_files.append(name[0:-3])
    break


if not os.path.exists(service_folder):
    os.makedirs(service_folder)

for filename in os.listdir(service_folder):
    file_path = os.path.join(service_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_path, e))


for idx, service_file_name in enumerate(service_files):
    with open(
        os.path.join(service_folder, service_file_name + ".service"),
        "w",
        encoding="utf8",
    ) as fp:
        fp.write("[Unit]\n")
        fp.write("Description=" + service_file_name + "\n")
        fp.write("After=multi-user.target\n")
        fp.write("Conflicts=getty@tty1.service\n\n")
        fp.write("[Service]\n")
        fp.write("Type=simple\n")
        fp.write("User=" + user + "\n")
        fp.write("Group=" + user + "\n")
        fp.write(
            "ExecStart=/usr/bin/python3 "
            + os.path.join(pwd, service_file_name + ".py")
            + " -c "
            + config_file
            + "\n"
        )
        fp.write("StandardInput=tty-force\n")
        fp.write("Restart=always\n")
        fp.write("RestartSec=5s\n\n")
        fp.write("[Install]\n")
        fp.write("WantedBy=multi-user.target\n\n")
        fp.close()
