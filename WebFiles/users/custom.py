""" 
Python file for custom functions
Author: @Abhinand D Manoj
Date: 28 Jan 2022
"""

import datetime 

def calculate(alarms: object) -> object:
    ''' Function to calculate nearest alarm '''

    times = [i.time for i in alarms]
    now = datetime.datetime.now().time()

    try:
        youngest = min([dt for dt in times if dt > now])
    except ValueError:
        return None
    else:
        return alarms[times.index(youngest)]