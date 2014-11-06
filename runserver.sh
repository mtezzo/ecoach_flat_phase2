#!/bin/sh

if [[ $1 == "selector" ]] ; then
    source /usr/local/ecoach_webapps/env/v1/bin/activate
    cd /usr/local/ecoach_webapps
    python manage.py runserver localhost:80 --settings=myselector.settings
elif [[ $1 == "mts2" ]] ; then
    source /usr/local/ecoach_webapps/env/v1/bin/activate
    cd /usr/local/ecoach_webapps
    python manage.py runserver localhost:80 --settings=mydata2.settings
else
    echo "myrunserver < selector | mts0 | mts1 | ... | mtsX > to pick app"
fi
