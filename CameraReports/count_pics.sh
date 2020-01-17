#!/bin/bash

cd ../RAWSTORAGE

newestdir=$(ls | tail -n1)

#echo $newestdir > ../CameraReports/latestday.txt

cd $newestdir

echo "Camera, nPictures" > ../../CameraReports/noplatest.csv

for i in $(seq 1 180); do
    numberofpics=$(ls "Cam$i"_* | wc -l )
    echo Cam"$i", $numberofpics >> ../../CameraReports/noplatest.csv
done