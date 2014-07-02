#!/bin/bash

#export SCRIPT_DIR=$(pwd)

echo 'begin script' 
cd ~jtritz/bitbucket/ecoach_webapps/mydata9/mts9
svn update
#svn update -r1445 mts.dictionary
source ~jtritz/virtualenv/v1/bin/activate
python ~jtritz/bitbucket/ecoach_webapps/manage.py collectstatic --noinput --settings=mydata9.settings
echo 'end of script'




