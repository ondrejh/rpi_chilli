#!/usr/bin/gnuplot

set xdata time
set style data lines
set term png size 800,400
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H"
set xlabel "time [h]"
set ylabel "humidity [%]"
set y2label "temperature [°C]"
set autoscale y
set autoscale y2
set autoscale x
set y2tics autofreq
set output filename.'.png'
set datafile separator ','
set grid
plot filename.'.tmp' using 1:2 t "humi" w lines linewidth 2.5 axes x1y1, filename.'.tmp' using 1:3 t "temp" w lines linewidth 2.5 axes x1y2
