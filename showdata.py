#!/usr/bin/python

import pymysql.cursors
import datetime

#database
db_name = 'chilli'
table_name = 'logdata'

connection = pymysql.connect(host='localhost',user='root',password='1234')
connection.autocommit(True) #this is magic (it doesn't work without)

with connection.cursor() as cursor:
    #get last timestamp
    sql = "select max(tstamp) from {}.{}".format(db_name,table_name)
    lts = cur.fetchall()[0][0]
    print(lts)

    tmin = lts - datetime.timedelta(1,0,0)

    sql = "select * from {}.{} where tstamp >= {}".format(db_name,table_name,tmin)
    cur.execute(sql)
    ret = cur.fetchall()
    print(ret)

    cursor.close()

connection.close()
