# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 19:55:11 2017

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
end_date = datetime.today()
date_fmt = "%Y-%m-%d"

conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
c = conn.cursor()
print("Opened database successfully")

cursor = c.execute("SELECT LAST_TRADE_DAY from stockdata order by LAST_TRADE_DAY desc limit 0,1")
tmp=cursor.fetchall()
start_yesdate = tmp[0][0][0:10]  #找到数据库中最近一次的更新日期  字符串格式
print("The latest date in Database is : "+start_yesdate)
start_date = datetime.strptime(start_yesdate,date_fmt)+timedelta(days = 1)#已经找到！起始日期！日期格式
print("Start Date is : "+str(start_date)[0:10])


#找到并判别成份股列表
codedict = {}
date_tmp = str('date=' + str(datetime.today())[0:10] + ';windcode='+indexcode)
wset = w.wset("sectorconstituent",date_tmp)
codedict[str(datetime.today())[0:10]] = wset.Data[1]
windcode_tmp = codedict[str(datetime.today())[0:10]]
#wind中更新这天的成份股列表

cursor = c.execute("SELECT * from codelist")
pin = cursor.fetchall()
pin = pin[-1]
tmp=[]
for i in range(0,len(pin)):
    tmp.append(pin[i])
key = tmp[0]
dict={}
tmp.remove(tmp[0])
dict[key]=tmp #将成份股列表中的最后一行转换为字典，利用列表进行判断
#print(dict)
print("Code list is : \n")
print(tmp)
#数据库中最新的成份股列表

#起始日的成份股列表
codedict1 = {}
date_tmp = str('date=' + str(start_date)[0:10] + ';windcode='+indexcode)
wset = w.wset("sectorconstituent",date_tmp)
codedict1[str(start_date)[0:10]] = wset.Data[1]
tmp1 = codedict1[str(start_date)[0:10]]

if tmp == windcode_tmp:  #A2
    for code in tmp:   
        print("Searching data for "+code+'...')
        dayprice = pd.DataFrame(columns=[])
        fm = pd.DataFrame(columns=[])
        conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        cursor = c.execute("SELECT LAST_TRADE_DAY from stockdata WHERE TRADE_CODE='"+ code[0:6] +"' order by LAST_TRADE_DAY desc limit 0,1")
        strtdate=cursor.fetchall()
        strtdate=strtdate[0][0][0:10]
        statdate=datetime.strptime(strtdate,date_fmt)
        statdate=statdate+timedelta(days=1)
        statdate=str(statdate)[0:10]
        wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", statdate, str(datetime.today()), "")
        fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
        dayprice = dayprice.append(fm.T,ignore_index=True)
        cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
        cnx.commit()
    print("Update Complete!")
elif tmp != windcode_tmp: #A1
#    向数据库codelist表中新增一条codelist记录，然后找寻每支股票最后一次的更新时间，如果找不到，就从当日开始记录，如果找到了，就从最后一次的时间进行更新   
    if tmp1 == tmp:  #A12
        end_date1 = datetime.strptime(str(start_date)[0:10],date_fmt)+timedelta(days=15)
        wtday = w.tdays(start_date, str(end_date1)[0:10], "")
        trdays = wtday.Times
        list=[]
        for trday in trdays:
            list.append(str(trday)[0:10])
        if start_date in list: #A122
            start_date = start_date
        elif start_date not in list:#A121
            start_date = list[0]
        date_sensor = datetime.strptime(start_date,date_fmt) #datetime类型    
        while date_sensor <= datetime.strptime(str(datetime.today())[0:10],date_fmt):
            print("Searching for codelist on " + str(date_sensor)[0:10] + "...")
            date_tmp = str('date=' + str(date_sensor) + str(';windcode='+indexcode))#取得当天成份股详情
            wset = w.wset("sectorconstituent",date_tmp)
            codedict_tmp =  wset.Data[1]  #存放date_sensor寻找到的当日的成份股列表
            if codedict_tmp == tmp1:#如果date_sensor找到的成份股列表与字典中第一条记录
                date_sensor = date_sensor + timedelta(days = 1)  #date_sensor前进一日
            elif codedict_tmp != tmp1:   #如果找到的成份股列表与之前的不同
                codedict1[str(date_sensor)[0:10]] = wset.Data[1]   #将其取出，放入dict中，此前，dict中有一个元素：起始日第二天：成份股列表
                tmp1 = codedict1[str(date_sensor)[0:10]]   #tmp1变为最新一次成份股更改的成份股列表
                date_sensor = date_sensor + timedelta(days = 1) #日期前进一天
        codeSeries = pd.Series(codedict1)   #讲所有的成份股更改日期与成份股列表放入series中，
        #print(codeSeries)
        strdatelist = []   #新建一个空列表，放入日期格式的成份股更改日期
        for i in range(0,len(codeSeries.index)):
            strdatelist.append(codeSeries.index[i])
        #print(strdatelist)
        alter_datelist=[]#新建一个空列表，放入字符串型的成份股更改日期
        for strdate in strdatelist:
            alter_datelist.append(datetime.strptime(strdate,date_fmt))
        #print(alter_datelist)
        time_tag_datetmp =  datetime.strptime(start_date,date_fmt) #时间指针从起始日开始
        #print(time_tag_datetmp)
        end_date12 = alter_datelist[0]+timedelta(days=15)
        wtday1 = w.tdays(start_date, str(end_date1)[0:10], "")
        trdays1 = wtday1.Times
        list1=[]
        for trday in trdays1:
            list1.append(str(trday)[0:10])
        if str(alter_datelist[0])[0:10] in list1:
            time_tag_datetmp = alter_datelist[0]
        elif trday not in list1:
            time_tag_datetmp = datetime.strptime(list1[0],date_fmt)
            del alter_datelist[0]
        #print(time_tag_datetmp)
        for k in range(0,len(alter_datelist)-1):
                print("***********") 
                print("k = ",k)
                dayprice = pd.DataFrame(columns=[])
                print(time_tag_datetmp)
                print(alter_datelist[k])
                if time_tag_datetmp>=alter_datelist[k] and time_tag_datetmp<alter_datelist[k+1]:
                    code_list = codeSeries.loc[str(alter_datelist[k])[0:10]]
                    start_date_tag = str(alter_datelist[k])[0:10] #+timedelta(days=1))[0:10] 
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
                cnx.commit()   
                time_tag_datetmp = alter_datelist[k]
                print(time_tag_datetmp)
                print("k = ",k)
                print("###############")
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
            print(str(end_date_tag)[0:10])
            wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", start_date_tag, end_date_tag, "")
            fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
            dayprice = dayprice.append(fm.T,ignore_index=True)
        cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
        cnx.commit()
        codeSeries = pd.Series(codedict1)
        code_frame_tmp = pd.DataFrame(codedict1)
        code_frame_tmp = code_frame_tmp.drop([code_frame_tmp.columns[0]],axis=1)
#        code_frame_tmp = pd.DataFrame(code_frame_tmp[str(start_date)[0:10]],columns=[str(start_date)[0:10]])
#        code_frame_tmp = code_frame_tmp.drop([str(start_date)[0:10]],axis=1)
        con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        con.commit()
        code_frame = pd.DataFrame(code_frame_tmp.T)
        code_frame.to_sql('codelist',con,if_exists='append')
        con.commit()
    elif tmp1 != tmp:  #A11  
        date_sensor = start_date #datetime类型    
        while date_sensor <= datetime.strptime(str(datetime.today())[0:10],date_fmt):
            print("Searching for codelist on " + str(date_sensor)[0:10] + "...")
            date_tmp = str('date=' + str(date_sensor) + str(';windcode='+indexcode))#取得当天成份股详情
            wset = w.wset("sectorconstituent",date_tmp)
            codedict_tmp =  wset.Data[1]  #存放date_sensor寻找到的当日的成份股列表
            if codedict_tmp == tmp1:#如果date_sensor找到的成份股列表与字典中第一条记录
                date_sensor = date_sensor + timedelta(days = 1)  #date_sensor前进一日
            elif codedict_tmp != tmp1:   #如果找到的成份股列表与之前的不同
                codedict1[str(date_sensor)[0:10]] = wset.Data[1]   #将其取出，放入dict中，此前，dict中有一个元素：起始日第二天：成份股列表
                tmp1 = codedict1[str(date_sensor)[0:10]]   #tmp1变为最新一次成份股更改的成份股列表
                date_sensor = date_sensor + timedelta(days = 1) #日期前进一天
        codeSeries = pd.Series(codedict1)   #讲所有的成份股更改日期与成份股列表放入series中，
        strdatelist = []   #新建一个空列表，放入日期格式的成份股更改日期
        for i in range(0,len(codeSeries.index)):
            strdatelist.append(codeSeries.index[i])
        alter_datelist=[]#新建一个空列表，放入字符串型的成份股更改日期
        for strdate in strdatelist:
            alter_datelist.append(datetime.strptime(strdate,date_fmt))
        time_tag_datetmp =  start_date #时间指针从起始日开始
        for k in range(0,len(alter_datelist)-1):
                print("***********") 
                print("k = ",k)
                dayprice = pd.DataFrame(columns=[])
                if time_tag_datetmp>=alter_datelist[k] and time_tag_datetmp<alter_datelist[k+1]:
                    code_list = codeSeries.loc[str(alter_datelist[k])[0:10]]
                    start_date_tag = str(alter_datelist[k]+timedelta(days=1))[0:10] 
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
                cnx.commit()   
                time_tag_datetmp = alter_datelist[k]
                print(time_tag_datetmp)
                print("k = ",k)
                print("###############")
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
            print(str(end_date_tag)[0:10])
            wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", start_date_tag, end_date_tag, "")
            fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
            dayprice = dayprice.append(fm.T,ignore_index=True)
        cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
        cnx.commit()
        codeSeries = pd.Series(codedict1)
        code_frame_tmp = pd.DataFrame(codedict1)
        con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        con.commit()
        code_frame = pd.DataFrame(code_frame_tmp.T)
        code_frame.to_sql('codelist',con,if_exists='append')
        con.commit()


      
