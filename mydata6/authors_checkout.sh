#!/bin/bash

#export SCRIPT_DIR=$(pwd)

echo 'begin script' 
cd ~jtritz/bitbucket/ecoach_webapps/mydata6/mts6
svn update
#svn update -r1424 mts.dictionary
#svn update -r1636 mts.dictionary
source ~jtritz/virtualenv/v1/bin/activate
python ~jtritz/bitbucket/ecoach_webapps/manage.py collectstatic --noinput --settings=mydata6.settings
echo 'end of script'




