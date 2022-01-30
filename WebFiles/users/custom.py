""" 
Python file for custom functions
Author: @Abhinand D Manoj
Date: 28 Jan 2022
"""

import datetime 

def calculate(alarms: object) -> object:
    ''' Function to calculate nearest alarm '''

    try:
        times = [datetime.datetime.strptime(i.time, '%H:%M:%S').time() for i in alarms]
        now = datetime.datetime.now().time()
        youngest = min([dt for dt in times if dt > now])
    except ValueError:
        return None
    else:
        return alarms[times.index(youngest)]