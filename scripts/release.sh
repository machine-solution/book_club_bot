#! /bin/bash

cd ~/book_club/book_club_bot/

.scripts/update.sh &&
sudo systemctl restart script &&
echo "$(date +%F::%T) Project released successfully" >> ~/logs/shell.log

cd --
