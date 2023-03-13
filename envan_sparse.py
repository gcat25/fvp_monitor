#!/usr/bin/python3
"""
version 1.0.0 --- changelog
1) New struct as multipage dash app (details here: https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91)
Present file becomes app included in global structure
"""
import pandas as pd
global_constants = {
    "LOG_FILE": 'env_an.log',
    "MAX_ATTEMPT": 3,
    "SW_VERSION": "1.0.0"
}

def mlog(type, message):
    f_out = open(global_constants["LOG_FILE"], "a+")
    current_timestamp = str(pd.to_datetime('today'))
    log_rec = current_timestamp + ':  ' + message
    print(f'{current_timestamp}:  {type} - {message}', file=f_out)
    f_out.close()
