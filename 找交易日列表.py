# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:42:16 2017

@author: jinjianfei
"""

from WindPy import w
w.start()

import numpy as np
import pandas as pd
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta

path = 'C:/Users/jinjianfei/Desktop/'
indexcode = "000016.SH"
start_date = "2017-01-26"
end_date = datetime.today()
date_fmt = "%Y-%m-%d"

end_date = datetime.strptime(start_date,date_fmt)+timedelta(days=15)
wtday = w.tdays(start_date, str(end_date)[0:10], "")
trdays = wtday.Times
list=[]
for trday in trdays:
    list.append(str(trday)[0:10])
print(list)

if start_date in list:
    start_date = start_date
elif start_date not in list:
    start_date = list[0]
print(start_date)