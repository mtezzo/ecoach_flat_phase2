#!/bin/sh

if [[ $1 == "selector" ]] ; then
    source /var/www/ecoach_webapps/env/v1/bin/activate
    cd /var/www/ecoach_webapps
    python manage.py runserver localhost:8000 --settings=myselector.settings
elif [[ $1 == "mtsdemo" ]] ; then
    source /var/www/ecoach_webapps/env/v1/bin/activate
    cd /var/www/ecoach_webapps
    #python manage.py runserver localhost:8000 --settings=mydata22.settings
    python manage.py runserver localhost:80 --settings=mydatademo.settings
    #sudo python manage.py runserver localhost:80 --settings=mydata17.settings
else
    echo "myrunserver < selector | mts0 | mts1 | ... | mtsX > to pick app"
fi
