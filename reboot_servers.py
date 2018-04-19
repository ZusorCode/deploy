from tinydb import TinyDB
import subprocess
def reload():
    config_db = TinyDB('config.json')
    subprocess.call('sudo pkill gunicorn', shell=True)
    subprocess.call('sudo pkill gunicorn3', shell=True)
    for item in config_db.all():
        subprocess.call('sudo gunicorn --chdir /home/tobi/server/%s -b 127.0.0.1:%s %s:app --daemon'
        % (item['folder'], item['port'], item['app_name']), shell=True)
    subprocess.call('sudo pkill linx', shell=True)
    subprocess.call('cd ../server/files/ && sudo nohup ./linx -bind 127.0.0.1:7931 &', shell=True)
    subprocess.call('systemctl reload nginx.service', shell=True)

if __name__ == "__main__":
    reload()
