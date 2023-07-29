#! /bin/bash

cd ~/book_club/book_club_bot/

echo "$(date +%F::%T) Start release" >> ~/logs/shell.log

scripts/update.sh &&
sudo systemctl restart script >> ~/logs/shell.log

code=$?

if [[ e == 0 ]]; then
    echo "$(date +%F::%T) Success release" >> ~/logs/shell.log
else
    echo "$(date +%F::%T) Fail release" >> ~/logs/shell.log
fi

cd --

exit $code
