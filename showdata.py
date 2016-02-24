#!/usr/bin/python

import pymysql.cursors
import datetime
import subprocess

def printnice(ret,filename=None):
    if filename==None:
        for row in ret:
            print('{},{:0.01f},{:0.01f}'.format(row[0],row[1],row[2]))
    else:
        with open(filename,'w') as file:
            for row in ret:
                file.write('{},{},{}\n'.format(row[0],row[1],row[2]))
            file.close()

#database
db_name = 'chilli'
table_name = 'logdata'

connection = pymysql.connect(host='localhost',user='root',password='1234')
connection.autocommit(True) #this is magic (it doesn't work without)

with connection.cursor() as cur:
    #get last timestamp
    sql = "select max(tstamp) from {}.{}".format(db_name,table_name)
    cur.execute(sql)
    lts = cur.fetchall()[0][0]
    
    #create filename
    fname = datetime.date.strftime(lts,'/tmp/chilli_%y%m%d_%H%M')

    tmin = lts - datetime.timedelta(1,0,0,0,0,0)

    sql = '''select * from {}.{} where tstamp >= "{}"'''.format(db_name,table_name,tmin)
    cur.execute(sql)
    ret = cur.fetchall()

    subprocess.call('''rm /tmp/chilli_*''',shell=True)

    printnice(ret,'{}.tmp'.format(fname))
    subprocess.call('''/usr/bin/gnuplot -e "filename='{}'" /home/pi/plotfile.gp'''.format(fname),shell=True)

    cur.close()

connection.close()
