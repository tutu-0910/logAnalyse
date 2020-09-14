#!/bin/sh
mysql -hlocalhost -uroot -p'123123' -e"$1"  gitlog >/home/logAnalyse/logAnalyse/gitlogStatic/logfile/$2.xls
exit 0
