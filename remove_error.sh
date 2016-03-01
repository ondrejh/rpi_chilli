#!/bin/bash

mysql -u root -p1234 -e "delete from chilli.logdata where humidity>100;"
