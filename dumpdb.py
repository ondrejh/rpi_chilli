#!/usr/bin/python3

""" dump db to see if data storing works well """

import sqlite3
import sys

# database
db_name = '/var/www/html/sensor.sql'
table_name = 'data'


def dump_db(db, table):

    conn = sqlite3.connect(db)
    c = conn.cursor()

    query = "SELECT * FROM {}".format(table)
    c.execute(query)

    data = c.fetchall()

    conn.close()

    return data


if __name__ == "__main__":

    db_name = db_name

    if len(sys.argv) > 1:
        db_name = sys.argv[1]

    data = dump_db(db_name, table_name)

    for d in data:
        print("{} {:.2f}% {:.2f}°C".format(d[3], d[2], d[1]))
