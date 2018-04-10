#!/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install nginx python3 python3-pip software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo pip3 install tinydb, flask
