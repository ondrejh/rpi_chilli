#!/bin/bash

DATE=$(date +"%Y%m%d_%H%M")

raspistill -w 800 -h 600 -o /var/www/html/archive/$DATE.jpg

cp /var/www/html/archive/$DATE.jpg /var/www/html/chilli.jpg
