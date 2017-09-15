# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:35:10 2017

@author: jinjianfei
"""


import sqlite3 as sq3
import pandas as pd
import numpy as np

path = 'C:/Users/jinjianfei/.spyder2-py3/'
query = 'CREATE TABLE 资料 (代码  PRIMARY text ,价格 real,简称 text,评级 text, 剩余期限 real,估值 real,前一日估值 real,债券类别 text,成交日期 date)'
con = sq3.connect(path+'最终.db')
con.commit()
df = pd.read_excel('Excel文件.xlsx',index_col='代码')
df.to_sql('最终',con)
con.commit()








# 可成功读取Excel文件，转换为pandas的dataframe格式，然后存储到sqlite中。数据库文件有一个表“资料”，数据库文件名为“最终.db”