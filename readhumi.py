#!/usr/bin/python3

""" this should read humidity and temperature from DHT sensor and store it into sqlite db file
to run this every 5 minutes do following:
	sudo crontab -e

	insert into the last line: */ * * * * python /home/pi/readhumi.py
"""

import Adafruit_DHT
import sqlite3

# sensor connection
pin = 4
sensor = Adafruit_DHT.AM2302

# database
db_name = '/var/www/html/sensor.sql'
table_name = 'data'


def read_values():

	humi, temp = Adafruit_DHT.read_retry(sensor, pin)

	if humi > 100:
		humi, temp = Adafruit_DHT.read_retry(sensor, pin)

	if humi <= 100:
		return humi, temp

	return None, None


def write_db(db, table, humidity, temperature):

	conn = sqlite3.connect(db)
	c = conn.cursor()

	query = "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, humidity REAL, temperature REAL, timestamp \
	DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table)
	c.execute(query)

	h = round(humidity, 2)
	t = round(temperature, 2)
	query = "INSERT INTO {} (temperature, humidity) VALUES ({}, {})".format(table, h, t)
	c.execute(query)

	conn.commit()
	conn.close()


def dump_db(db, table):

	conn = sqlite3.connect(db)
	c = conn.cursor()

	query = "SELECT * FROM {}".format(table)
	c.execute(query)

	data = c.fetchall()

	conn.close()

	return data


if __name__ == "__main__":

	import sys

	if (len(sys.argv) > 1) and sys.argv[1] == 'dump':
		data = dump_db(db_name, table_name)
		for d in data:
			print("{} {:.2f}% {:.2f}°C".format(d[3], d[2], d[1]))
		exit()

	h, t = read_values()

	if h is not None:

		if (len(sys.argv) > 1) and sys.argv[1] == 'test':
			print("Humidity: {}\nTemperature: {}".format(round(h, 2), round(t, 2)))
		else:
			write_db(db_name, table_name, h, t)
