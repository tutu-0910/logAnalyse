#!/bin/sh
mysqldump  -u root  -p'123123'  --databases khatch --tables khatch_api_gitlogpubstat  --where=analyze_id=$1 > /home/gitlog/$2/$3.sql

exit 0
