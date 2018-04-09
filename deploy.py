import subprocess
print("This will add a new Flask app to nginx and modify the files needed for that")
print("Current apps")
with open('config', 'r') as f:
    print("Current apps")
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        print(line)
domain = input("Domain name: ")
repository = input("Repository name: ")
url = input("Repository URL: ")
port = input("Port for gunicorn: ")
confirm = input("Confirm: ")
if confirm != "y":
    exit()
subprocess.call("git clone %s" % url, shell=True)

with open('/etc/nginx/sites-enabled/default', 'a') as file:
    file.write("""
server {
        server_name %s;
        location / {
                proxy_pass http://127.0.0.1:%s;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                }
        }
    """ %(domain, port))

with open('reboot_servers.sh', 'a') as script:
    script.write("""
cd /home/tobi/server/%s
sudo gunicorn -b 127.0.0.1:%s app:app --daemon
    """ %(repository, port))

with open('config', 'a') as config:
    config.write("%s %s" % (repository, port))

subprocess.call("sudo certbot -d %s --nginx" % domain, shell=True)
subprocess.call("sudo ./reboot_servers.sh", shell=True)
