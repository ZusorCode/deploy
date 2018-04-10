#!/bin/bash
sudo apt-get --yes --force-yes update
sudo apt-get --yes --force-yes upgrade
sudo apt-get --yes --force-yes install nginx python3 python3-pip software-properties-common
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get --yes --force-yes upgrade update
sudo apt-get --yes --force-yes upgrade install python-certbot-nginx
sudo pip3 install tinydb, flask
