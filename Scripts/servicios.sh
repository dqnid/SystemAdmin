#!/bin/sh

servicios=("sshd" "apache2" "postfix" "mariadb")
dir="/var/www/html/servicios/"
for i in "${servicios[@]}"
do
    activo=$(systemctl is-active $i)
    if [[ "$activo" == "active" ]]; then
        echo 1 > "$dir$i"
    else
        echo 0 > "$dir$i"
    fi
done
