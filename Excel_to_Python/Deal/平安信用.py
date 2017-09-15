# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 08:25:12 2017

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
filename = '信唐成交.txt'
start_date = "2016-08-01"
end_date = "2017-08-13"
date_fmt = "%Y-%m-%d"

class Deal():
    """平安信用ok
       平安利率 少价格
       BGC利率OK
       BGC信用 有\t
       国际信用  缺价格，多%
       国际利率 少部门缺价格
       国利利率 有\t
       国利信用 有\t
       信唐成交  缺价格、多空格    
    """
    def __init__(self):
        """"""
    
    def pingan_credit(self):
        with open(path+filename) as file_object:
        #    contents = file_object.read()
        #    print(contents)
            for line in file_object:
                if len(line)>10:
                    list = line.split(' ')
                    list1 = []
                    for a in list:
                        if len(a)!=0:
                            if '\n' not in a:
                                list1.append(a)
                            elif '\n' in a:
                                list1.append(a[:-1])
#                    print(list1)
                    for i in list1:
                        list2 = []
                        if re.match(r'^([0-9]{1,}[.][0-9]*)$', i):
                            list2.append(i)
                            for j in list1:
                                if re.match(r'^\d{9}|^\d{7}|^\d{6}|^\d{6}.[SH]|^\d{6}.[SZ]$', j):
                                    list2.append(j)
                    print(list2)                    
 

a = Deal()
a.pingan_credit()

            
