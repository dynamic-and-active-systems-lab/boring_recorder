#!/bin/bash
#use sudo chmod +x /home/dasl/repos/boring_recorder/resetRecorder.sh
#in terminal to make this file executable. Otherwise you'll get
#a permission denied error.

#Zip up all the files
zipName=$(date +/home/dasl/Desktop/%Y_%m_%d-%H_%M_%S.zip)
echo ARCHIVING RECORDINGS TO $zipName
zip $zipName /home/dasl/Desktop/Recordings/*
zip -ur $zipName /home/dasl/repos/boring_recorder/mycrontablog.txt
#Trash the old files and clear out the log file 
gio trash /home/dasl/Desktop/Recordings/* 
echo "" > /home/dasl/repos/boring_recorder/mycrontablog.txt