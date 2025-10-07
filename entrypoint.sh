#!/bin/sh

ln -s /db/evennia.db3 /app/server/evennia.db3
pip install --upgrade pip
pip install --upgrade -r requirements.txt
evennia ipstart
