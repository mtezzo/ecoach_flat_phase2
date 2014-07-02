#!/bin/bash

# This is a horable hack to allow the MTS devleopers to reboot the server
# Basically, they create the flag file refrenced below and a root cron job hits this script once per minute

# BE SURE TO ADJUST THIS PATH!!!
if [ -f '/home/jtritz/bitbucket/ecoach_webapps/reboot_flag.txt' ]; then
    /sbin/service httpd restart
    echo $USER > '/home/jtritz/bitbucket/ecoach_webapps/done.txt'
    rm '/home/jtritz/bitbucket/ecoach_webapps/reboot_flag.txt'
fi

