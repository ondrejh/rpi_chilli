#!/bin/bash

rm out.mp4

ffmpeg -framerate 5 -pattern_type glob -i "2022*.jpg" -c:v libx264 -vf fps=25,format=yuv420p out.mp4

mv out.mp4 video.mp4
