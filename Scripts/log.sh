#!/bin/sh
a=$(date)
echo "$a : $1" >> /var/log/login.log
