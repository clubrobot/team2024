#!/bin/bash

if [ $# -ne 2 ]
then
    echo "Usage : $0 dossier_synchronise adresse_raspberry_pi" >&2
    exit 1
fi
rsync -r -u --delete -e ssh --progress  --exclude-from=".syncignore" "$1" pi@$2:/home/pi/ClubRobot/team2024