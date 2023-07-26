#! /bin/bash

cd ~/book_club/book_club_bot/

git fetch --all
git reset --hard origin/main
chmod -R +x scripts # make permissions to execute all files in this folder

cd --
