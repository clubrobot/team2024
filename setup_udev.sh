#!/bin/bash

PYTHONPATH=$(python3 -m site --user-site)

REPOSITORY="/home/pi/ClubRobot/team2024"

UDEVRULES_DIRECTORY=/etc/udev/rules.d
UDEVRULE='KERNEL=="ttyUSB*", PROGRAM="/usr/bin/env PATH='"$PATH"' PYTHONPATH='"$PYTHONPATH:$REPOSITORY/raspberrypi/"' '"$REPOSITORY/raspberrypi/robot getuuid"' /dev/%k", SYMLINK+="arduino/%c" \nKERNEL=="ttyACM*" , PROGRAM="/usr/bin/env PATH='"$PATH"' PYTHONPATH='"$PYTHONPATH:$REPOSITORY/raspberrypi/"' '"$REPOSITORY/raspberrypi/robot getuuid"' /dev/%k", SYMLINK+="arduino/%c" '
#UDEVRULE='KERNEL=="ttyUSB*", PROGRAM="/usr/bin/env PATH='"$PATH"' PYTHONPATH='"$PYTHONPATH:$REPOSITORY/raspbe>RULEFILE="$UDEVRULES_DIRECTORY/99-serialtalks.rules" '
RULEFILE="$UDEVRULES_DIRECTORY/99-serialtalks.rules"

if [ ! -e "$RULEFILE" ]
then
        sudo usermod -aG dialout $USER
        echo -e "$UDEVRULE" | sudo tee "$RULEFILE"
        sudo udevadm control --reload-rules
fi