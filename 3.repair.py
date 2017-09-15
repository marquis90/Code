# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 19:26:11 2017

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
end_date = str(datetime.today())[0:10]
date_fmt = "%Y-%m-%d"
time_fmt = " %H:%M:%S.%f"

def qu_cha_ji(seta,setb):
    list1=list2=[]
    list1 = seta
    list2 = setb
    cha_ji = list(set(list1)^set(list2))
    return cha_ji
############################################################################
####################第一步，找到缺失的整个交易日##############################
############################################################################
print("Processing Preliminary Diagnosis...")
conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
c = conn.cursor()
print("\nOpened Database Successfully")
cursor = c.execute("SELECT distinct LAST_TRADE_DAY from stockdata ")
tmp=cursor.fetchall()
bd_date_list=[]
for date in tmp:
    bd_date_list.append(date[0][0:10])
wtdays=w.tdays(start_date, end_date, "")
wind_date_list_tmp = wtdays.Times
wind_date_list=[]
for d in wind_date_list_tmp:
    wind_date_list.append(str(d)[0:10])
repair_date_tmp = qu_cha_ji(wind_date_list,bd_date_list)#需要修复的整日日期，datetime格式
repair_date = []
for dat in repair_date_tmp:
    repair_date.append(str(dat)[0:10])
if repair_date:#要修理
    print("\nMissing Date is : ")
    print(repair_date)#字符型的日期格式
    print("\nStep 1 :补全缺失整日数据")
else :
    print("\nNo Missing Tradedays!")

for date in repair_date:#取出需要修复当日的成份股列表
    date_tmp = str('date=' +date+ ';windcode='+indexcode)
    wset = w.wset("sectorconstituent",date_tmp)
    code_list = wset.Data[1]
    dayprice = pd.DataFrame(columns=[])
    dayprice_tmp = pd.DataFrame(columns=[])
    for code in code_list:
        print("\nSearching Data for "+code+" on "+date+"...")
        print("Writing Data...")
        fm = pd.DataFrame(columns=[])
        wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume",date,date, "")
        fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
        dayprice_tmp = dayprice_tmp.append(fm.T,ignore_index=True)
    dayprice = dayprice.append(dayprice_tmp)
    cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
    pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
    cnx.commit() 
print("Step 1 Complete!")
print("Processing Further Diagnosis")
############################################################################
####################第二步，找到缺失的单支股票################################
############################################################################      
print("\nStep 2 :补全单支股票缺失数据")
conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
c = conn.cursor()
print("\n********Opened Database Successfully******")
#db_date_list元素为字符型完整格式日期
cursor = c.execute("SELECT distinct LAST_TRADE_DAY from stockdata ")
tmp=cursor.fetchall()
db_date_list=[]
for i in range(0,len(tmp)):
    db_date_list.append(tmp[i][0])
#已找到数据库中所有的交易日

#找到每日的成份股，并计数
miss_dates = []
for db_date in db_date_list:
    conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
    c = conn.cursor()
    cursor = c.execute("SELECT TRADE_CODE from stockdata WHERE LAST_TRADE_DAY='"+db_date+"'")
    code_tmp=cursor.fetchall()
    code_list = []
#    print(code_tmp)
    for code in code_tmp:
        code_list.append(code[0])
#    print(code_list)
    if len(code_list) == 50:
        pass
    elif len(code_list) != 50:
#        print(db_date[0:10]+" is missing! ")
        miss_dates.append(db_date)
if miss_dates:
    print("\n********These days' data is not complete********\n")
    for miss_date in miss_dates:
        print(miss_date[0:10])
    print("**********************************************")
    #miss_dates中为完整日期格式的字符串日期
    for miss_date in miss_dates:
        date_tmp = str('date=' +miss_date[0:10]+ ';windcode='+indexcode)
        wset = w.wset("sectorconstituent",date_tmp)
        wind_code_list_tmp = wset.Data[1]
        wind_code_list = []
        for wind_code in wind_code_list_tmp:
            wind_code_list.append(wind_code[0:6])
    #    print(wind_code_list)
        cursor = c.execute("SELECT TRADE_CODE from stockdata WHERE LAST_TRADE_DAY='"+miss_date+"'")
        code_temp = cursor.fetchall()
        db_code_list = []
        for code in code_temp:
            db_code_list.append(code[0])
        mis_code = qu_cha_ji(db_code_list,wind_code_list)
        print("\nMiss stock code(s) on "+miss_date[0:10])
        print(mis_code)
        dayprice = pd.DataFrame(columns=[])
        for mcode in mis_code:
            if mcode[0] =='6':
                mcode = mcode+".SH"
            elif mcode[0] =='0':
                mcode = mcode+".SZ"
            elif mcode[0] =='3':
                mcode = mcode+".SZ"
            print("\nSearching Data for "+mcode+" on "+miss_date[0:10]+"...")
            print("Writing Data...")
            fm = pd.DataFrame(columns=[])
            wsd = w.wsd(mcode, "last_trade_day,trade_code,open,high,low,close,volume",miss_date[0:10],miss_date[0:10], "")
            fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
            print(fm)
            dayprice = dayprice.append(fm.T,ignore_index=True)
            print(dayprice)
        cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        pd.DataFrame.to_sql(dayprice, name='stockdata',con=cnx, if_exists='append',index =False)
        cnx.commit()
    print("Repair Complete!")
else:
    print("Nothing further needs to be done !")
    










    
    