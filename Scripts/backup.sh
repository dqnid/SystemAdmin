#!/bin/sh

for dir in /home/*; do
    if [ $2 -eq 0 ]; then
        rsync -r $dir /root/BackUp
    else
        tar -cf "/root/BackUp/${dir:6}.tar" $dir
    fi
done
