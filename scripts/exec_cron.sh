#!/bin/bash

cd /home/machine_solution/book_club/book_club_bot

if [ $# -eq 0 ]; then
    echo "$(date +%F::%T) Cron file must be specified" >> /home/machine_solution/logs/shell.log
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "$(date +%F::%T) Cron file '$1' is not exists" >> /home/machine_solution/logs/shell.log
    exit 1
fi

if [ ! -x "$1" ]; then
    echo "$(date +%F::%T) Cron file '$1' is not executable" >> /home/machine_solution/logs/shell.log
    exit 1
fi


echo "$(date +%F::%T) Cron file '$1' run" >> /home/machine_solution/logs/shell.log

source venv/bin/activate
python "$1" >> /home/machine_solution/logs/shell.log
deactivate

cd -
