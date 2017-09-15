# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:39:01 2017

@author: jinjianfei
"""

from WindPy import w
w.start()

import numpy as np
import pandas as pd
import datetime
from pandas.io import sql
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta


path = 'C:/Users/jinjianfei/Desktop/'
indexcode = "000016.SH"
start_date = "2016-08-01"
end_date = "2017-08-13"
date_fmt = "%Y-%m-%d"

codedict = {}
date_tmp = str('date=' + start_date + ';windcode='+indexcode)
wset = w.wset("sectorconstituent",date_tmp)
codedict[start_date] = wset.Data[1]
tmp = codedict[start_date]

date_sensor = datetime.strptime(start_date,date_fmt) + timedelta(days = 1)  #datetime类型
while date_sensor <= datetime.strptime(end_date,date_fmt):
    print("Searching for codelist on " + str(date_sensor)[0:10] + "...")
    date_tmp = str('date=' + str(date_sensor) + str(';windcode='+indexcode))#取得当天成份股详情
    wset = w.wset("sectorconstituent",date_tmp)
    codedict_tmp =  wset.Data[1]
    if codedict_tmp == tmp:
        date_sensor = date_sensor + timedelta(days = 1)
    elif codedict_tmp != codedict[start_date]:
        codedict[str(date_sensor)[0:10]] = wset.Data[1]
        tmp = codedict[str(date_sensor)[0:10]]
        date_sensor = date_sensor + timedelta(days = 1)

codeSeries = pd.Series(codedict)
code_frame_tmp = pd.DataFrame(codedict)
query = 'CREATE TABLE codelist ()'
con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
con.commit()
code_frame = pd.DataFrame(code_frame_tmp.T)
code_frame.to_sql('codelist',con)
con.commit()                         

#字符日期转换为datetime格式： 
#1\datetime.strptime(字符串，字符格式“%Y-%m-%d %H:%M:S”);
#2\日期格式转换为字符串格式，使用——str（日期）[0:10]，可以取出‘xxxx-xx-xx’格式。
time_tag = start_date   #取股票用到的时间标签，与key做对比
time_tag_datetmp = datetime.strptime(time_tag,date_fmt)  #将其转换为datetime格式
strdatelist = []  
for i in range(0,len(codeSeries.index)):
    strdatelist.append(codeSeries.index[i])

alter_datelist=[]
for strdate in strdatelist:
    alter_datelist.append(datetime.strptime(strdate,"%Y-%m-%d"))    

path = 'C:/Users/jinjianfei/Desktop/'
query = 'CREATE TABLE stockdata (date  date ,code  text,open float,high float,low float, close float,volume  float)'
con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
con.commit()

for k in range(0,len(alter_datelist)-1):
    print("***********") 
    print("k = ",k)
    dayprice = pd.DataFrame(columns=[])
    if time_tag_datetmp>=alter_datelist[k] and time_tag_datetmp<alter_datelist[k+1]:
        code_list = codeSeries.loc[str(alter_datelist[k])[0:10]]
        start_date_tag = str(alter_datelist[k])[0:10] 
        end_date_tag = str(alter_datelist[k+1]+timedelta(days = -1))[0:10]
        print(code_list)
        print(start_date_tag)
        print(end_date_tag)
        dayprice_tmp = pd.DataFrame(columns=[])
        for code in code_list:
            print("Searching data for " + code + "...")
            print(start_date_tag)
            print(end_date_tag)
            fm = pd.DataFrame(columns=[])
            wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", start_date_tag,end_date_tag, "")
            fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
            dayprice_tmp = dayprice_tmp.append(fm.T,ignore_index=True)
        dayprice = dayprice.append(dayprice_tmp)
        print(dayprice)
        k=k+1
        print("k = ",k)
        print("!!!")
        print(time_tag_datetmp>=alter_datelist[k])    
    cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
    pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
    con.commit()   
    time_tag_datetmp = alter_datelist[k]
    print(time_tag_datetmp)
    print("k = ",k)
    print("###############")
con.commit()       

print("Processing the last component...")         
start_date_tag =  str(alter_datelist[-1])[0:10]
end_date_tag = end_date
code_list = codeSeries.loc[str(alter_datelist[-1])[0:10]]
print(code_list)
print(start_date_tag)
print(end_date_tag)
dayprice = pd.DataFrame(columns=[])
fm = pd.DataFrame(columns=[])
for code in code_list:
    print("Searching data for " + code + "...")
    print(start_date_tag)
    print(end_date_tag)
    wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", start_date_tag, end_date_tag, "")
    fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
    dayprice = dayprice.append(fm.T,ignore_index=True)
cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
con.commit()
