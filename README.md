RPi based chilli seeds greenhouse monitor
=========================================

## Hardware:

BOM: Raspberry PI, Rpi camera, FPV BEC, 12V white LED strips, 12V cooling fan, NPN transistors, resistors, DHT22 humidity sensor, 12V power supply, seed starter greenhouse 

![Fritzing schematic - colorfull and useless](/doc/schema.png)

## Instalation on Raspbian Stretch (Lite):

Change pasword (but don't forget it).

	passwd

Update system.

	sudo apt-get update
	sudo apt-get upgrade

Enable camera and ssh, set timezone.

	sudo raspi-config

Install packages.

- git .. get repository
- python3_pip .. install python libraries
- apache2 .. web server
- wiringpi .. switch on - off light and fan
- did I forget something?


	sudo apt-get install git python3_pip apache2 wiringpi

Install python dht library using pip.

	sudo pip3 install adafruit_dht
	
Clone rpi_chilli (this) repository.

	git clone https://github.com/ondrejh/rpi_chilli.git

Install (copy) web page.

	sudo cp rpi_chilli/www/* /var/www/html/

Test light, fan and camera.

	./lightOn.sh
	./lightOff.sh
	./fanOn.sh
	./fanOff.sh

	sudo ./capture.sh	

Setup crontab to run scripts automatically.

	sudo crontab -c
	
	# add lines:

	*/15 * * * * /home/pi/rpi_chilli/readhumi.py
	
	0 6 * * * /home/pi/rpi_chilli/lightOn.sh
	0 21 * * * /home/pi/rpi_chilli/lightOff.sh
    
	0 7,10,13,16,19 * * * /home/pi/rpi_chilli/fanOn.sh
	15 7,10,13,16,19 * * * /home/pi/rpi_chilli/fanOff.sh

	30 7,10,13,16,19 * * * /home/pi/rpi_chilli/capture.sh

## Backend script files:

- readhumi.py .. read humidity and temperature from DHT sensor and save in into database
- capture.sh  .. captures camera picture with time stamp
- lightOn.sh  .. turn light on
- lightOff.sh .. turn light off
- fanOn.sh    .. turn fan on
- fanOff.sh   .. turn fan off

## ToDo:

- fan PWM
- dawn, dusk
- some doc picture
- simple schematic
