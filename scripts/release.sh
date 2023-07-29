#! /bin/bash

cd ~/book_club/book_club_bot/

scripts/update.sh &&
sudo systemctl restart script

code=$?

if [[ e == 0 ]]; then
    echo "$(date +%F::%T) Success release" >> ~/logs/shell.log
else
    echo "$(date +%F::%T) Fail release" >> ~/logs/shell.log
fi

cd --

exit $code
