#!/bin/bash
TZ="UTC-1" date +%d-%m-%Y@%T\ -0100 >> /home/pi/fvp/dust.log
sleep 5
wget -qO - http://192.168.3.184 | \
 grep dust | sed s/\<tr\>\<td\>// | \
 sed s/\<\\/td\>\<td\>/,/ | \
 sed s/\<\\/td\>\<\\/tr\>// \
 >> /home/pi/fvp/dust.log

echo '********' >> /home/pi/fvp/dust.log
sleep 20

/home/pi/fvp/dust_log_2_csv.sh


