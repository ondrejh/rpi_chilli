#!/bin/bash

DATE=$(date +"%Y%m%d_%H%M")

raspistill -w 640 -h 480 -o /var/www/html/archive/$DATE.jpg

cp /var/www/html/archive/$DATE.jpg /var/www/html/chilli.jpg
