#!/bin/bash

#export SCRIPT_DIR=$(pwd)

echo 'begin script' 
cd ~jtritz/bitbucket/ecoach_webapps/mts/mts19
svn update
#svn update -r1445 mts.dictionary
source ~jtritz/virtualenv/v1/bin/activate
python ~jtritz/bitbucket/ecoach_webapps/manage.py collectstatic --noinput --settings=mydata19.settings
echo 'end of script'




