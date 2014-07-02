#!/bin/sh

if [[ $1 == "selector" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=myselector.settings
elif [[ $1 == "mts6" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata6.settings
elif [[ $1 == "mts7" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata7.settings
elif [[ $1 == "mts8" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata8.settings
elif [[ $1 == "mts9" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata9.settings
elif [[ $1 == "mts14" ]] ; then
    source ~/virtualenv/v4/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata14.settings
elif [[ $1 == "mts16" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata16.settings
elif [[ $1 == "mts17" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata17.settings
elif [[ $1 == "mts18" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata18.settings
elif [[ $1 == "mts19" ]] ; then
    source ~/virtualenv/v1/bin/activate
    cd ~/bitbucket/ecoach_webapps
    sudo python manage.py runserver localhost:80 --settings=mydata19.settings
else
    echo "myrunserver < selector | mts0 | mts1 | ... | mtsX > to pick app"
fi



