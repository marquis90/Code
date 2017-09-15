# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 08:58:35 2017

@author: jinjianfei
"""

import numpy as np
import pandas as pd
import sqlite3 as sq3
from datetime import datetime, date, time, timedelta

from WindPy import w
w.start()

path = 'C:/Users/jinjianfei/Desktop/'
indexcode = "000016.SH"
end_date = datetime.today()
date_fmt = "%Y-%m-%d"

class Update():
    """类有三个形参：代码、起始日期、截止日期"""
    
    def __init__(self,code,start_date,end_date):#ok
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
    
    def get_start_date(self):#ok
        """从数据库中寻找最后一次出现数据的日期，加一日，作为起始日,字符串格式，"%Y-%m-%d" """
        conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        c = conn.cursor()
        cursor = c.execute("SELECT LAST_TRADE_DAY from stockdata order by LAST_TRADE_DAY desc limit 0,1")
        statdate=str(datetime.strptime(cursor.fetchall()[0][0][0:10],date_fmt)+timedelta(days=1))[0:10]
        return statdate
    
    def get_end_date(self):#ok
        """以更新当日作为截止日期，字符串格式，"%Y-%m-%d" """
        self.end_date = str(datetime.today())[0:10]
        return self.end_date
    
    def get_dbcodelist(self):#ok
        """从数据库codelist表中，取出最新一次的成份股，返回列表形式"""
        con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        c = con.cursor()
        cursor = c.execute("SELECT * from codelist")
        pin = cursor.fetchall()[-1] #取出数据库中codelist所有内容，取最新一次的成份股
        dbcodelist=[pi for pi in pin][1:]
        return dbcodelist
        
    def get_wdcodelist(self):#ok
        """从万得中取出更新当日的成份股，返回列表形式"""
        codedict = {}
        date_tmp = str('date=' + str(datetime.today())[0:10] + ';windcode='+indexcode)
        wset = w.wset("sectorconstituent",date_tmp)
        codedict[str(datetime.today())[0:10]] = wset.Data[1]
        windcode = codedict[str(datetime.today())[0:10]]
        return windcode
    
    def update_codelist(self):#ok
        """更新成分股列表，并写入数据库codelist表中：
        利用get_start_date()找到起始日，在万得中！！逐日提取当日成份股列表B1，
        与get_dbcodelist()得到的列表B2对比，并循环至更新日。
        如果，B1=B2，日期加1天，继续循环；如果不相等，将日期做键，万得取出的列表为值，
        组成字典，写入数据库codelist表中，循环此过程。"""
        date_sensor = datetime.strptime(self.get_start_date(),date_fmt)  #datetime类型
        tmp = self.get_dbcodelist()
        codedict = {}
        while date_sensor <= datetime.strptime(self.get_end_date(),date_fmt):
            print("Searching for codelist on " + str(date_sensor)[0:10] + "...")
            wind_tmp = str('date=' + str(date_sensor) + str(';windcode='+indexcode))
            wset = w.wset("sectorconstituent",wind_tmp)
            codedict_tmp =  wset.Data[1]#w万得当日的成份股详情
            if codedict_tmp == tmp:
                date_sensor = date_sensor + timedelta(days = 1)
            elif codedict_tmp != tmp:
                codedict[str(date_sensor)[0:10]] = wset.Data[1]
                tmp = codedict[str(date_sensor)[0:10]]
                date_sensor = date_sensor + timedelta(days = 1)
        print("Total update "+str(len(codedict))+" code list(s).")
        code_frame_tmp = pd.DataFrame(codedict)
        con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        code_frame = pd.DataFrame(code_frame_tmp.T)
        code_frame.to_sql('codelist',con,if_exists='append')
        con.commit()
        codeSeries = pd.Series(codedict)
        return codeSeries        
        
    def unchange_update(self):#ok
        """如果成份股列表没有发生变化，则按照这个方法进行后续更新。
           取出每个成份股在数据库中的最后一条数据对应的日期，以这个日期作为起始日期，
           进行!逐个股票!检查更新写入过程"""
        codelist = self.get_dbcodelist()
        for code in codelist:   
            print("Searching data for "+code+'...')
            print("Writing data...")
            wsd = w.wsd(code, "last_trade_day,trade_code,open,high,low,close,volume", self.get_start_date, str(datetime.today()), "")
            dayprice = pd.DataFrame(columns=[])
            fm = pd.DataFrame(columns=[])
            fm=pd.DataFrame(wsd.Data,index=wsd.Fields,columns=wsd.Times)
            dayprice = dayprice.append(fm.T,ignore_index=True)
            cnx = sq3.connect(path+str(indexcode[0:6]+'data.db'))
            pd.DataFrame.to_sql(dayprice, name='stockdata', con=cnx, if_exists='append',index =False)
            cnx.commit()
        print("\nUpdate Complete!")    
    
    
    def judge_code(self):
        """对数据库中的codelist最新一条数据与万得更新当日的成份股明细进行对比
           如果成份股没有发生变化，则利用数据库中的最新成份股列表对个股！！逐个进行更新，
           如果成份股明细发生变化，首先更新数据库codelist表"""
        if self.get_wdcodelist() == self.get_dbcodelist():
            print("\nCode List does not change!\n")
            print("Updating...\n")
            self.unchange_update()
        else:
            print("not ok")
            self.update_codelist()
            
a=Update('','','')
#a.judge_code()
a.update_codelist()







