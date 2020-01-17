#!/bin/bash

## CD into main directory
cd ../2018PIPELINE

## Loading Latex and R
source /com/extra/texlive/2016/load.sh
source /com/extra/R/3.5.0/load.sh
## Activate conda environment CameraReports (Standard py2.7 install)
source activate CameraReports

## Local scripts used to list the files for transfer
f=$(./list.sh | grep selftest | tail -n1)

## Downloading the latest file called selftest, and deleting them in the
echo "Downloading $f"
./download.sh $f CameraReports/$f
./delete.sh $f
./cleancloud.sh selftest

## Moving to the CameraReport directory.
cd CameraReports

## Remove any old system error file
rm SYSTEM_ERROR

## Process the Camera status file. Example file found on github, under name selftest.
python ProcessCameraStatus.py $f

## Using Slurm to send an email to maintainers, if there is a critical error. (SYSTEM_ERROR file is produced byProcessCameraStatus.py if there occurs an error)
if [ -e SYSTEM_ERROR ]; then
    sbatch --mail-type=BEGIN --mail-user="emailaddress@domain.com" --job-name="IMAGE SYSTEM DOWN" -o "%x-latest.out" ls.sh
fi

## Count the number of images taken in the latest day.
./count_pics.sh

cd /home/marnit/NChain/faststorage/WHITE_CLOVER/2018PIPELINE/CameraReports

## Collecting latest sample images of each camera.
./fetch_pics.sh

source activate CameraReports

## Producing camera report.
python camreport.py
rm $f
## Committing the latest report to git.
git add camreport.md
git add camreport_files/figure-markdown_github/unnamed-chunk-3-1.svg
git add pictures/
git add -u
git commit -m "Latest status"
rm camreport.csv

## It is pushed to git later in a different file.
