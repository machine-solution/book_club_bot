#!/bin/bash

cd /home/machine_solution/book_club/book_club_bot

scripts/update.sh
scripts/kill.sh # service will be restarted automaticly by systemctl

cd -
