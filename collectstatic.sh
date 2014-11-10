#!/bin/bash

export SCRIPT_DIR=$(pwd)

echo "-------running collectstatic------"

source /var/www/ecoach_webapps/env/v1/bin/activate

python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydatademo.settings


echo 'done'

