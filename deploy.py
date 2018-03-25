import os
print("This will add a new Flask app to nginx and modify the files needed for that")
domain = input("Domain name: ")
with open('config', 'r') as f:
    print("Current apps")
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        print(line)
port = input("Port for gunicorn: ")
confirm = input("Confirm: ")
if confirm != "y":
    exit()
if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
