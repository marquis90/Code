# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 17:10:34 2017

@author: jinjianfei
"""


import numpy as np
import pandas as pd
import datetime
from pandas.io import sql
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta


path = 'C:/Users/jinjianfei/Desktop/'
indexcode = "000016.SH"


conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
c = conn.cursor()
cursor = c.execute("SELECT * from stockdata order by TRADE_CODE asc")
conn.commit()