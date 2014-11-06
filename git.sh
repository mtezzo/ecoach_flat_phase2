#!/bin/bash

projects=(.\/
djangotailoring
surveytracking
tailoring2
myauth
myselector
mytailoring
mypublisher
myloader
myexporter
myemailer
myusage
mylogger
nts
mydata2
)

#export SCRIPT_DIR=$(cd ..; pwd)
export SCRIPT_DIR=$(pwd)

for i in "${projects[@]}"
do
    printf "\n----------$i--------------\n"
    #cd $SRC_DIR\/$i
    cd $SCRIPT_DIR\/$i
    git $1
done

exit

mydata14

