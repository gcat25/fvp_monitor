#!/bin/bash
sed -n '
	/-0100/ {
		N
		{
		/-0100.*voltage/ {
			s/\n/,/
			N
			/density/ {
				/voltage.*density/ {
					s/\n/,/
					P
					}
				}
			}
		}

	}' /home/pi/fvp/dust.log > /home/pi/fvp/dust-log.csv
