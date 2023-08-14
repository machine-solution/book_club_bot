# bin/bash

cd ~/Documents/book_club/book_club_bot

if [ $# -eq 0 ]; then
    echo "$(date +%F::%T) Cron file must be specified" >> ~/logs/shell.log
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "$(date +%F::%T) Cron file '$1' is not exists" >> ~/logs/shell.log
    exit 1
fi

if [ ! -x "$1" ]; then
    echo "$(date +%F::%T) Cron file '$1' is not executable" >> ~/logs/shell.log
    exit 1
fi


echo "$(date +%F::%T) Cron file '$1' run" #>> ~/logs/shell.log

source venv/bin/activate
python "$1" #>> ~/logs/shell.log
deactivate

cd --
