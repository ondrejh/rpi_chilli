#!/bin/bash

if ! command -v rsync &> /dev/null
then
	# if not rsync installed just delete and copy
	rm -rf *.jpg
	scp pi@rpichilli.local:/var/www/html/archive/*.jpg .
else
	# if installed, better rsync it
	rsync pi@rpichilli.local:/var/www/html/archive/*.jpg .
fi

