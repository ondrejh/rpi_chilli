#!/usr/bin/python

''' this should read humidity and temperature from DHT sensor and store it into mysql database
to run this every 5 minutes do following:
	sudo crontab -e

	insert into the last line: */ * * * * python /home/pi/readhumi.py
'''

import Adafruit_DHT
import pymysql.cursors

#sensor connection
pin = 4
sensor = Adafruit_DHT.AM2302

#database
db_name = 'chilli'
table_name = 'logdata'

humi,temp = Adafruit_DHT.read_retry(sensor,pin)
#print('{:0.01f}% {:0.01f}*'.format(humi,temp))

connection = pymysql.connect(host='localhost',user='root',password='1234')
connection.autocommit(True)

with connection.cursor() as cursor:
	sql = "INSERT INTO {}.{}(humidity,temperature) VALUES ({:0.1f},{:0.1f})".format(db_name,table_name,humi,temp)
	#print(sql)
	cursor.execute(sql)
	cursor.close()

connection.close()
