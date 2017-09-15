# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:28:15 2017

@author: jinjianfei
"""

from api import Kata
import numpy as np
import pandas as pd
import datetime
from pandas.io import sql
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta

path = 'C:/Users/jinjianfei/Desktop/'
indexcode = "000016.SH"
date_fmt = "%Y-%m-%d"
time_fmt = " %H:%M:%S.%f"

"""Kata(代码(支持列表输入),开盘价,最高价,最低价,收盘价,成交量,个股大小判断(大于、小于、等于),排序关键词,排序方式)"""

"""取个股时间段内数据"""
a = Kata('code=600000','keyword1=OPEN','keyword2=HIGH','keyword3=LOW','keyword4=CLOSE','keyword4=','start_date=2016-08-12','end_date=2016-08-20','order_condition=open>16.5','order_keyword=open','order_way=asc')
a.get_detail()


"""取某日成份股列表"""
#b = Kata('','','','','','','start_date=2016-08-12','','','','')
#b.indexconstituent()

"""取一段时间内的交易日"""
#b = Kata('','','','','','','start_date=2017-07-15','end_date=2017-08-11','','','')
#b.get_traday()

"""计算一段时间相隔的交易日数量"""
#b = Kata('','','','','','','start_date=2017-08-08','end_date=2017-08-11','','','')
#b.cal_traday()
