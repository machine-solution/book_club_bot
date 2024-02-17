#!/bin/bash

cd /home/machine_solution/book_club/book_club_bot/

echo "$(date +%F::%T) Start release" >> /home/machine_solution/logs/shell.log

scripts/update.sh >> /home/machine_solution/logs/shell.log

code=$?

if [[ $code == 0 ]]; then
    source venv/bin/activate
    python -m pip install -r requirements.txt &&
    sudo systemctl restart script >> /home/machine_solution/logs/shell.log
else
    exit $code
fi

code=$?

if [[ $code == 0 ]]; then
    echo "$(date +%F::%T) Success release" >> /home/machine_solution/logs/shell.log
    scripts/kill.sh >> /home/machine_solution/logs/shell.log
    # service will be restarted automaticly by systemctl
else
    echo "$(date +%F::%T) Fail release" >> /home/machine_solution/logs/shell.log
fi

cd -

exit $code
