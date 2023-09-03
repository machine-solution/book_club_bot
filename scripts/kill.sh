#!/bin/bash

ps -e | grep -h "python" | awk -F '[^0-9]+' '{ print $2 }' | xargs kill ||
echo "old processes already dead"
