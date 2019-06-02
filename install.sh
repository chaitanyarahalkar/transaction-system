#!/bin/sh

virtualenv env 
source env/bin/activate

pip3 install -r requirements.txt

echo "Successfully installed all packages!"
sleep(1)
echo "Starting Django server"

python3 manage.py runserver



