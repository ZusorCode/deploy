from tinydb import TinyDB
import subprocess
def reload():
    config_db = TinyDB('config.json')
    subprocess.call('sudo pkill gunicorn', shell=True)
    subprocess.call('sudo pkill gunicorn3', shell=True)
    for item in config_db.all():
        subprocess.call('cd /home/tobi/server/%s' % item['folder'], shell=True)
        subprocess.call('sudo gunicorn3 -b 127.0.0.1:%s %s:app --daemon'
        % (item['port'], item['app_name']), shell=True)
    subprocess.call('systemctl reload nginx.service', shell=True)

if __name__ == "__main__":
    reload()