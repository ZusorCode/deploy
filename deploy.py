import os
if os.getuid() != 0:
    print("You need to run this script as root!")
    exit()

import subprocess, random
from tinydb import TinyDB
import re
from tools import config, reboot_servers
config_db = TinyDB('config.json')
action = input("(d)eploy or (r)emove: ")
if not action in ['d', 'r', 'D', 'R']:
    print("Fatal: Unknown Command")
    exit()
if action in ['d', 'D']:
    domain = input("Domain name: ")
    repo_url = input("Repository URL: ")
    name = re.findall(r"([^\/]+)\.git$", repo_url)
    if name:
        name = name[0]
    else:
        print("Error: Name of repository couldn't be determined automatically")
        name = input("Repository name: ")
    port = random.randint(3000,9000)
    subprocess.call("clear", shell=True)
    print("------------------------------------------")
    print("Domain: %s" % domain)
    print("Repository URL: %s" % repo_url)
    print("Repository name: %s" % name)
    print("Port chosen: %s" % port)
    print("------------------------------------------")
    confirm = input("Confirm (y/n) ")
    if confirm != "y":
        print("Fatal: No confirmation!")
        exit()
    print("Cloning repository")
    subprocess.call("git clone %s ../%s -q" % (repo_url, name), shell=True)
    print("Creating nginx config")
    config.create_config(domain, port, name)
    print("Getting certificate")
    subprocess.call("sudo certbot -d %s --nginx --redirect -n " % domain, shell=True)
    print("Adding to simple_deploy config")
    config_db.insert({'domain': domain, 'port': port, 'folder': name})
    print("Reloading server")
    reboot_servers.reload()
