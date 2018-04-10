from tinydb import TinyDB
db = TinyDB('config.json')
while True:
    domain = input("Domain: ")
    port = input("Port: ")
    folder = input("Folder name: ")
    db.insert({"folder": folder, "port": port, "domain": domain})
    print("Next")
