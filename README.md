RPi based chilli seeds greenhouse monitor
=========================================

## Hardware:

This is how it looks now:

![Snapshot](doc/snapshot_description.jpg)

BOM: Raspberry PI, Rpi camera, FPV BEC, 12V white LED strips, 12V cooling fan, NPN transistors, resistors, DHT22 humidity sensor, 12V power supply, seed starter greenhouse 

![Fritzing schematic - colorfull and useless](doc/schema.png)

## Instalation on Raspbian Stretch (Lite):

Change pasword (but don't forget it).

	passwd

Update system.

	sudo apt-get update
	sudo apt-get upgrade

Enable camera and ssh, set timezone.

	sudo raspi-config

Install packages.

	sudo apt-get install git python3-pip
	sudo apt-get isntall apache2 php libapache2-mod-php php-sqlite3
	sudo apt-get install wiringpi

- git .. get repository
- python3_pip .. install python libraries
- apache2 .. web server
- php, libapache2-mod-php .. php
- php-sqlite3 .. sqlite database support for php
- wiringpi .. switch on - off light and fan

Install python dht library and flask (micro web framework) using pip.

	sudo pip3 install adafruit_dht
	sudo pip3 install flask
	sudo pip3 install RPi.GPIO
	
Clone rpi_chilli (this) repository.

	git clone https://github.com/ondrejh/rpi_chilli.git

Install (copy) web page.

	sudo cp -r rpi_chilli/www/* /var/www/html/

Test light, fan and camera.

	./lightOn.sh
	./lightOff.sh
	./fanOn.sh
	./fanOff.sh

	sudo ./capture.sh

Install condition controll service.

	sudo cp condcontrol.service /lib/systemd/system/
	sudo chmod 644 /lib/systemd/system/condcontrol.service
	sudo systemctl daemon-reload
	sudo systemctl enable condcontrol.service
	sudo systemctl start condcontrol.service

Setup crontab to run scripts automatically.

	sudo crontab -e
	
	# add lines:

	*/15 * * * * /home/pi/rpi_chilli/readhumi.py
	
	30 7,10,13,16,19 * * * /home/pi/rpi_chilli/capture.sh

## Backend script files:

- readhumi.py .. read humidity and temperature from DHT sensor and save in into database
- capture.sh  .. captures camera picture with time stamp
- lightOn.sh  .. turn light on
- lightOff.sh .. turn light off
- fanOn.sh    .. turn fan on
- fanOff.sh   .. turn fan off
- condcontrol.py .. service scrip for gpio pwm with flask interface
- condcontrol.service .. start file

## ToDo:

- service setup and web interface
- timelapse video
