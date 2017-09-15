# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:15:14 2017

@author: jinjianfei
"""
import numpy as np
import pandas as pd
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta

path = 'C:/Users/jinjianfei/Desktop/'
date_fmt = "%Y-%m-%d"
indexcode = "000016.SH"

conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
c = conn.cursor()
print("Opened database successfully")
cursor = c.execute("SELECT * from codelist")
pin = cursor.fetchall()   #3个元组组成的列表

list=[]
for j in range(0,len(pin)):
    lis=[]
    for i in range(0,len(pin[j])):
        lis.append(pin[j][i])
    list.append(lis)
#print(list) #3个列表组成的列表

dict={}
for i in range(len(list)):
    key = list[i][0]
    del list[i][0]
    value = list[i]
    dict[key] = value
print(dict)#将从数据库中codelist表中取得的股票列表转换为字典的形式