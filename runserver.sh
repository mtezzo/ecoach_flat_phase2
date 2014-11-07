#!/bin/sh

if [[ $1 == "selector" ]] ; then
    source /var/www/ecoach_webapps/env/v1/bin/activate
    cd /var/www/ecoach_webapps
    python manage.py runserver localhost:8000 --settings=myselector.settings
elif [[ $1 == "mts22" ]] ; then
    echo 'here'
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    #python manage.py runserver localhost:8000 --settings=mydata22.settings
    sudo python manage.py runserver localhost:80 --settings=mydata22.settings
    #sudo python manage.py runserver localhost:80 --settings=mydata17.settings
else
    echo "myrunserver < selector | mts0 | mts1 | ... | mtsX > to pick app"
fi
