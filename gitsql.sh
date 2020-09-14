#!/bin/sh
mysqldump  -u root  -p'123123'  --databases gitlog --tables logAnalyse_gitlogpubstat  --where=analyze_id=$1 > /home/logAnalyse/logAnalyse/gitlogStatic/logfile/$2.sql

exit 0
