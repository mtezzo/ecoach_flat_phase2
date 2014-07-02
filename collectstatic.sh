#!/bin/bash

export SCRIPT_DIR=$(pwd)

echo "-------running collectstatic------"

source ~/virtualenv/v4/bin/activate

python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata6.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata7.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata8.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata9.settings

python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata16.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata17.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata18.settings
python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata19.settings

python $SCRIPT_DIR/manage.py collectstatic --noinput --settings=mydata14.settings

echo 'done'

