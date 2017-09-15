# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 19:12:33 2017

@author: jinjianfei
"""

#from WindPy import w
#w.start()

import numpy as np
import pandas as pd
import datetime
from pandas.io import sql
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta
import re


path = 'C:/Users/jinjianfei/Desktop/data/'
filename = '平安信用.txt'
start_date = "2016-08-01"
end_date = "2017-08-13"
date_fmt = "%Y-%m-%d"

f = open(path+filename, 'r')
str = f.readlines()   #整个txt文件是一个列表，每一行是一个元素
list = []
for i in str:
    list.append(i.split('\t'))
#print(list) #已无\t   #整个txt文件是一个列表，每一行是一个元素
for j in range(0,len(list)):
#    a = []
    for k in list[j]:
        a = []
        if k =="" or k =='\n':
            pass
        else:
            a.append(k)
            print(a)
            
            
            """每个要素是一个列表"""

    


