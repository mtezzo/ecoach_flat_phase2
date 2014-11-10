#!/bin/bash

#export SCRIPT_DIR=$(pwd)

echo 'begin script' 
cd /var/www/ecoach_webapps/mts/mtsdemo
svn update
#svn update -r1444 mts.dictionary
#svn update -r1574 mts.dictionary
source /var/www/ecoach_webapps/env/v1/bin/activate
python /var/www/ecoach_webapps/manage.py collectstatic --noinput --settings=mydatademo.settings
echo 'end of script'




