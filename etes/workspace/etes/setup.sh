#!/bin/bash
# Installation script for ETES.

# Environment setup

# Run in shell:
# adduser dev
# usermod -aG sudo dev
# su dev
# cd ~/
# scp etes.zip dev@74.207.249.78:~/
# sudo apt install -y unzip
# unzip etes.zip
# cd ~/etes
# bash setup.sh

sudo apt update
sudo apt install -y nginx python3-pip mysql-server

# MySQL

mysql -u root -p
# Enter in mysql:
# SET PASSWORD FOR root@localhost=PASSWORD(''); -- disable passwd for convenience
# CREATE USER 'tqtruong95'@'localhost';
# GRANT ALL PRIVILEGES ON * . * TO 'tqtruong95'@'localhost';
# FLUSH PRIVILEGES;
mysql -u root < etes.sql  # load db dump
sudo service mysql restart  # ensure running
mysql -u root --database etes_db --execute="SELECT event_id, name FROM event"  # ensure data exists

# Python & Flask

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install config files and set up nginx/wsgi interface

cd configs/
sudo cp etes /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/etes /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo cp flask-etes.service /etc/systemd/system/
sudo service nginx restart
cp -t ~/etes/ etes.ini wsgi.py

# start the etes application

sudo systemctl daemon-reload
sudo service flask-etes restart
