#!/bin/sh
sed '/@01.*PM/ {
		s/@01/@13/
	}' <dust.log >dust_log_formatted_3

sed '/@02.*PM/ {
		s/@02/@14/
	}' <dust_log_formatted_3 >dust_log_formatted_4

sed '/@03.*PM/ {
		s/@03/@15/
	}' <dust_log_formatted_4 >dust_log_formatted_5

sed '/@04.*PM/ {
		s/@04/@16/
	}' <dust_log_formatted_5 >dust_log_formatted_6

sed '/@05.*PM/ {
		s/@05/@17/
	}' <dust_log_formatted_6 >dust_log_formatted_7

sed '/@06.*PM/ {
		s/@06/@18/
	}' <dust_log_formatted_7 >dust_log_formatted_8

sed '/@07.*PM/ {
		s/@07/@19/
	}' <dust_log_formatted_8 >dust_log_formatted_9

sed '/@08.*PM/ {
		s/@08/@20/
	}' <dust_log_formatted_9 >dust_log_formatted_10

sed '/@09.*PM/ {
		s/@09/@21/
	}' <dust_log_formatted_10 >dust_log_formatted_11

sed '/@10.*PM/ {
		s/@10/@22/
	}' <dust_log_formatted_11 >dust_log_formatted_12

sed '/@11.*PM/ {
		s/@11/@23/
	}' <dust_log_formatted_12 >dust_log_formatted_13

sed '/@12.*PM/ {
		s/@12/@00/
	}' <dust_log_formatted_13 >dust_log_formatted_14


