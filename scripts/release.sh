#! /bin/bash

cd /home/machine_solution/book_club/book_club_bot/

echo "$(date +%F::%T) Start release" >> /home/machine_solution/logs/shell.log

scripts/update.sh &&
sudo systemctl restart script >> /home/machine_solution/logs/shell.log

code=$?

if [[ $code == 0 ]]; then
    echo "$(date +%F::%T) Success release" >> /home/machine_solution/logs/shell.log
else
    echo "$(date +%F::%T) Fail release" >> /home/machine_solution/logs/shell.log
fi

cd -

exit $code
