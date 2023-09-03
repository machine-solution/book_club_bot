#!/bin/bash

cd /home/machine_solution/book_club/book_club_bot

source venv/bin/activate
nohup python vk_bot/bot.py

cd -
