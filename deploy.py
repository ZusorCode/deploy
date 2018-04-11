import os, sys
if os.getuid() != 0:
    print("You need to run this script as root!")
    exit()

import subprocess, random
from tinydb import TinyDB, Query
import re
from tools import config, reboot_servers
import time

config_db = TinyDB('config.json')
action = input("(d)eploy or (r)emove: ")
if action in ['d', 'D']:
    domain = input("Domain name: ")
    repo_url = input("Repository URL: ")
    name = re.findall(r"([^\/]+)\.git$", repo_url)
    if name:
        name = name[0]
    else:
        print("Error: Name of repository couldn't be determined automatically")
        name = input("Repository name: ")
    app_name = input("Name of file to run: ")
    port = random.randint(3000,9000)
    subprocess.call("clear", shell=True)
    print("------------------------------------------")
    print("Domain: %s" % domain)
    print("Repository URL: %s" % repo_url)
    print("Repository name: %s" % name)
    print("Port chosen: %s" % port)
    print("File name: %s" % app_name)
    print("------------------------------------------")
    confirm = input("Confirm (y/n) ")
    if confirm != "y":
        print("Fatal: No confirmation!")
        exit()
    subprocess.call("git clone %s ../%s -q" % (repo_url, name), shell=True)
    config.create_config(domain, port, name)
    subprocess.call("sudo certbot -d %s --nginx --redirect -n -q" % domain, shell=True)
    config_db.insert({'domain': domain, 'port': port, 'folder': name, 'app_name': app_name})
    time.sleep(4)
    reboot_servers.reload()
    time.sleep(4)
    reboot_servers.reload()
    print("Done")
elif action in ['r', 'R']:
    for number, value in enumerate(config_db.all()):
        print("%s) %s" % (number + 1, value['folder']))
    selection = input("Select: ")

    try:
        selection = int(selection)
    except ValueError:
        exit()

    selection -= 1
    selected_folder = config_db.all()[selection]['folder']
    print("You selected %s" % selected_folder)
    confirm = input("Enter y to confirm: ")
    if confirm != "y":
        print("Cancelled")
        exit()
    search = Query()
    config_db.remove(search.folder == selected_folder)
    current_path = sys.path[0]
    subprocess.call("sudo rm -rf %s/../%s" % (current_path, selected_folder), shell=True)
    subprocess.call("sudo rm -rf /etc/nginx/sites-enabled/%s" % selected_folder, shell=True)
    time.sleep(4)
    reboot_servers.reload()
    print("Done")
else:
    print("Error")
    exit()
