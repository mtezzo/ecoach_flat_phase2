#!/bin/bash

#export SCRIPT_DIR=$(pwd)

echo 'begin script' 
cd /usr/local/ecoach_webapps/mts/mts2
svn update
#svn update -r1444 mts.dictionary
#svn update -r1574 mts.dictionary
source /usr/local/ecoach_webapps/env/v1/bin/activate
python /usr/local/ecoach_webapps/manage.py collectstatic --noinput --settings=mydata2.settings
echo 'end of script'




