RPi based chilli greenhouse monitor
===================================

files:

	readhumi.py .. read humidity and temperature from DHT sensor and save in into database
	gettable.sh .. print out log database table content
	
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
	
5) install apache:

	sudo apt-get install apache2

6) create entry in cron table (to make it run every 5 minutes):

	sudo crontab -e

	insert into the last line: "*/ * * * * /home/pi/runoften.sh"

