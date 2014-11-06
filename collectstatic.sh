#!/bin/bash

export SCRIPT_DIR=$(pwd)

echo "-------running collectstatic------"

source /usr/local/ecoach_webapps/env/v1/bin/activate

python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata2.settings


echo 'done'

