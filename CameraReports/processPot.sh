#!/bin/bash

source activate qrdetect

lastday=$(cat latestday.txt)
CAMS=$(cat $1)


echo "Pot,Size" > ../QRdetect/potsizes.csv

cd ../RAWSTORAGE/$lastday

for CAM in $CAMS;
do
    cam=${CAM%%,*}
    pot=${CAM##*,}
    echo "Camera:" $cam
    echo "Pot:" $pot

    latestpic=$(ls "$cam"_* | tail -n1 )
    echo "PROCESSING PICTURE: "$latestpic
    cp $latestpic ../../QRdetect/$latestpic
    cd ../../QRdetect
    python QRdetect.py -i $latestpic -o $latestpic -s potsizes.csv "$pot"
    cd ../RAWSTORAGE/$lastday
    
done

cd ../../QRdetect

mv potsizes.csv ../CameraReports/potsizes.csv
