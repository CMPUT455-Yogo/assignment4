#!/bin/bash
for i in $(seq 1 1 10)
    do
    echo "=========begin ${i} round========" >> game_log.txt
    python3 play.py >> game_log.txt
    echo "=========finish ${i} round========" >> game_log.txt
done


