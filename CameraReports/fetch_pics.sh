#!/bin/bash

lastday=$(cat latestday.txt)
cday=$(ls ../RAWSTORAGE | tail -n1)

echo $lastday
echo $cday

if [ "$cday" = "$lastday" ]
then
    echo "No new images"
else

    cd pictures

    rm *
    
    cd ..

    echo "Camera,CCODE,QRCODES,POTS" > ../tensorflow/summary.csv
    
    cd ../RAWSTORAGE
    
    echo "NEW IMAGES"

    echo $cday > ../CameraReports/latestday.txt

    cd $cday

    source activate tfcpu

    for i in $(seq 1 180); do
	latestpic=$(ls "Cam$i"_* | tail -n1 )
	echo "PROCESSING PICTURE: "$latestpic
	cp $latestpic ../../tensorflow/$latestpic
	cd ../../tensorflow
	python InferNetwork.py -i $latestpic -g clover_modelv3/frozen_inference_graph.pb -l clover_modelv3/label_map_clover.pbtxt -n 3 -d -o $latestpic
	mv $latestpic ../CameraReports/pictures/$latestpic
	cd ../RAWSTORAGE/$cday
    done

    cd ..

    echo $cday > ../CameraReports/latestday.txt
    cp ../QRdetect/summary.csv ../CameraReports/summary.csv 

fi
