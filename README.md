RPi based chilli greenhouse monitor
===================================

newsetup (1.2.2019):

install:

	# change pasword, update system, enable webcam and ssh

	passwd
	sudo apt-get update
	sudo apt-get upgrade
	sudo raspi-config

	# install packages:
	# git .. get repository
	# python3_pip .. install python libraries
	# apache2 .. web server
	# wiringpi .. switch on - off light and fan

	sudo apt-get install git python3_pip apache2 wiringpi

	# install python library (dht)

	sudo pip3 install adafruit_dht

	# get rpi_chilli repository
	git clone https://github.com/ondrejh/rpi_chilli.git

	# test ios
	./lightOn.sh
	./lightOff.sh
	./fanOn.sh
	./fanOff.sh

	# install web pages
	sudo cp www/* /var/www/html/

	# test webcam (enable in raspi-config first)
	sudo ./capture.sh	

	# set crontab
	sudo crontab -c
	# add lines:
	#
	#   */15 * * * * /home/pi/rpi_chilli/readhumi.py
	#
	#   0 6 * * * /home/pi/rpi_chilli/lightOn.sh
	#   0 21 * * * /home/pi/rpi_chilli/lightOff.sh

	#   0 7,10,13,15,17,19 * * * /home/pi/rpi_chilli/fanOn.sh
	#   15 7,10,13,15,17,19 * * * /home/pi/rpi_chilli/fanOff.sh

	#   30 7,10,13,16,19 * * * /home/pi/rpi_chilli/capture.sh


files:

	readhumi.py .. read humidity and temperature from DHT sensor and save in into database
	showdata.py .. get 1 day data from sql and draw the chart
	plotfile.gp .. plot data gnuplot script
	
	runoften.sh .. run readhumi.py and showdata.py to create fresh chart (called every 5 minutes)
	capture.sh  .. captures camera picture with time stamp (called every 15 minutes)
	
	lightOn.sh  .. turn light on
	lightOff.sh .. turn light off
	
installation steps:

1) install AdafruitDHT library:

	https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring

2) install mysql:

	#sudo apt-get install mysql-server mysql-client

3) create database:

	#mysql -u root -p
	
	mysql> create database chilli;
	mysql> use chilli;
	mysql> create table logdata (tstamp timestamp, humidity float, temperature float);
	mysql> quit;
	
4) install PyMySQL

	#sudo apt-get intall python-setuptools
	git clone https://github.com/PyMySQL/PyMySQL.git
	cd PyMySQL
	sudo python setup.py install
	
5) install apache and create dir for image archive:

	sudo apt-get install apache2

	sudo mkdir /var/www/html/archive
	
6) create entry in cron table (to make it run every 5 minutes):

	sudo crontab -e

	insert into the last lines: 
	
		*/5 * * * * /home/pi/runoften.sh
		*/15 * * * * /home/pi/capture.sh
		
		30 4 * * * /home/pi/lightOn.sh
		30 21 * * * /home/pi/lightOff.sh
