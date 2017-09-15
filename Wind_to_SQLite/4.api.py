# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:18:39 2017

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
date_fmt = "%Y-%m-%d"
time_fmt = " %H:%M:%S.%f"


"""Kata(代码(支持列表输入),开盘价,最高价,最低价,收盘价,成交量,个股大小判断(大于、小于、等于),排序关键词,排序方式)"""


class Kata():
    """ 相较qpitestffff增加多只股票查询"""
    
    def __init__(self,code,open,high,low,close,volume,start_date,end_date,con,order,order_way):
        """可以分别取某字段"""
        self.code = code[5:]
        self.open = open[9:]
        self.high = high[9:]
        self.low = low[9:]
        self.close = close[9:]
        self.volume = volume[9:]
        self.start_date = start_date[11:] + str(" 00:00:00.005000")
        self.end_date = end_date[9:] + str(" 00:00:00.005000")
        self.con = con[16:]
        self.order = order[14:]
        self.order_way = order_way[10:]
   
    def trade_dayt(self):
        """取出数据库中的所有交易日,字符串格式，"%Y-%m-%d %H:%M:%S.%f" """
        con = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        c = con.cursor()
        cursor = c.execute("SELECT distinct LAST_TRADE_DAY from stockdata ")
        bd_date_list = []
        for ddate in cursor.fetchall():
            bd_date_list.append(ddate[0])
        return bd_date_list
    
    def start_trade_day(self):
        """判断输入的开始日期是否在数据库中，如果不在返回最近交易日，字符串型完整格式"""
        lis_tmp = self.trade_dayt()
        while self.start_date not in lis_tmp:
            self.start_date = str(datetime.strptime(self.start_date,"%Y-%m-%d %H:%M:%S.%f")+timedelta(days = 1))
        return self.start_date
    
    def end_trade_day(self):
        """判断输入的截止日期是否在数据库中，如果不在返回最近交易日，字符串型完整格式"""
        lis_tmp = self.trade_dayt()
        while self.end_date not in lis_tmp:
            self.end_date = str(datetime.strptime(self.end_date,"%Y-%m-%d %H:%M:%S.%f")+timedelta(days = -1))
        return self.end_date
    
    def indexconstituent(self):
        """找到到开始日期当日的成份股列表"""
        lis_tmp = self.trade_dayt()
        print("\nStart Date is : " + self.start_date[0:10])
        while self.start_date not in lis_tmp:
            self.start_date = str(datetime.strptime(self.start_date,"%Y-%m-%d %H:%M:%S.%f")+timedelta(days = -1))
        print("\nThe Lastest Trade Day for Start Date is :" + self.start_date[0:10])
        conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
        c = conn.cursor()
        cursor = c.execute("SELECT TRADE_CODE from stockdata where LAST_TRADE_DAY='"+self.start_date+"'")
        tmp=cursor.fetchall()
        code_list = []
        for cod in tmp:
            code_list.append(cod[0])
        print("\nThe Constituent of " + indexcode + " is as followed:\n")
        print(code_list)
        return code_list
        
    def get_w_condi_list(self):
        """取得需要查询数据的字段，列表格式，用来生成dataframe的column是字段"""
        condi = []
        if len(self.open)!=0:
            condi.append('OPEN')
        if len(self.high)!=0:
            condi.append('HIGH')
        if len(self.low)!=0:
            condi.append('LOW')
        if len(self.close)!=0:
            condi.append('CLOSE')
        if len(self.volume)!=0:
            condi.append('VOLUME')
        return condi
    
    def get_w_condi_str(self):
        """取得需要查询数据的字段，字符格式，用来插入查询语句"""
        w_condi = 'LAST_TRADE_DAY,TRADE_CODE,'
        condi = self.get_w_condi_list()
        for word in condi:
            w_condi = w_condi+word+","
        w_condi = w_condi[:-1]
        return w_condi
    
    def get_keycondi(self):
        """对判断关键词‘con’进行判断与拆解"""
        cherector = ['>','<','=']
        listcon = []
        for c in cherector:
            if c in self.con:
                keycondi = self.con.split(c)[0]
                numcondi = self.con.split(c)[1]
                listcon.append(keycondi)
                listcon.append(c)
                listcon.append(numcondi)
            else:
                pass
        return listcon

    def split_code(self):
        """将以字符串格式输入的多个股票代码分开成单一股票并返回列表"""
        code_list = self.code.split(',')
        return code_list
        
    def get_detail_nullcon(self):#con条件为空
        """对日期循环取出个股的数据"""
        if len(self.order)==0 and len(self.order_way)==0:
            code_list = self.split_code()
            print("\nOpen Database Successfully !\n")
            dayprice = pd.DataFrame()
            for code in code_list:
                condi = self.get_w_condi_list()
                w_condi = self.get_w_condi_str()
                fields = ['LAST_TRADE_DAY', 'TRADE_CODE']+condi
                conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
                c = conn.cursor()
                cursor = c.execute("SELECT " + w_condi + " from stockdata where LAST_TRADE_DAY Between '"+self.start_date+"' and '"+self.end_date+"' AND TRADE_CODE='"+code+"'")
                tmp=cursor.fetchall()
                tmp_tmp = []
                for tup in tmp:  #元组转列表
                    tmp_tmp.append(list(tup))
                dict_index = []
                for g in tmp_tmp:#取字典的键
                    dict_index.append(g[0])
                dict = {}
                for o in range(0,len(dict_index)):#组成字典
                    dict[dict_index[o]] = tmp_tmp[o]
                dlist=list(dict.keys())
                fm = pd.DataFrame(dict,index = fields,columns = dlist)
                dayprice = dayprice.append(fm.T,ignore_index=True)
            print(dayprice)
        elif len(self.order)==0 and len(self.order_way)!=0:
            print("Please input sorting keyword!")
            print("\nBoth upper or lower case are accepted!")
        elif len(self.order)!=0 and len(self.order_way)==0:
            print("Please input sorting way including : 'asc' or 'dsec' !")
            print("\nBoth upper or lower case are accepted!")
        elif len(self.order)!=0 and len(self.order_way)!=0:
            print("\nOpen Database Successfully !\n")
            dayprice = pd.DataFrame()
            code_list = self.split_code()
            for code in code_list:
                condi = self.get_w_condi_list()
                w_condi = self.get_w_condi_str()
                fields = ['LAST_TRADE_DAY', 'TRADE_CODE']+condi
                conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
                c = conn.cursor()
                cursor = c.execute("SELECT " + w_condi + " from stockdata where LAST_TRADE_DAY Between '"+self.start_date+"' and '"+self.end_date+"' AND TRADE_CODE='"+code+"' order by "+self.order.upper()+" "+self.order_way)
                tmp=cursor.fetchall()
                tmp_tmp = []
                for tup in tmp:  #元组转列表
                    tmp_tmp.append(list(tup))
                dict_index = []
                for g in tmp_tmp:#取字典的键
                    dict_index.append(g[0])
                dict = {}
                for o in range(0,len(dict_index)):#组成字典
                    dict[dict_index[o]] = tmp_tmp[o]
                dlist=list(dict.keys())
                fm = pd.DataFrame(dict,index = fields,columns = dlist)
                dayprice = dayprice.append(fm.T,ignore_index=True)
            print(dayprice)            

    def get_detail_con(self):#con条件非空
        """对日期循环取出个股的数据"""
        scon = self.get_keycondi()
        if len(self.order)==0 and len(self.order_way)==0:
            print("\nOpen Database Successfully !\n")
            code_list = self.split_code()
            dayprice = pd.DataFrame()
            for code in code_list:
                condi = self.get_w_condi_list()
                w_condi = self.get_w_condi_str()
                fields = ['LAST_TRADE_DAY', 'TRADE_CODE']+condi
                conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
                c = conn.cursor()
                cursor = c.execute("SELECT " + w_condi + " from stockdata where LAST_TRADE_DAY Between '"+self.start_date+"' and '"+self.end_date+"' AND TRADE_CODE='"+code+"' AND "+scon[0].upper()+scon[1]+scon[2])
                tmp=cursor.fetchall()
                tmp_tmp = []
                for tup in tmp:  #元组转列表
                    tmp_tmp.append(list(tup))
                dict_index = []
                for g in tmp_tmp:#取字典的键
                    dict_index.append(g[0])
                dict = {}
                for o in range(0,len(dict_index)):#组成字典
                    dict[dict_index[o]] = tmp_tmp[o]
                dlist=list(dict.keys())
                fm = pd.DataFrame(dict,index = fields,columns = dlist)
                dayprice = dayprice.append(fm.T,ignore_index=True)
            print(dayprice)
        elif len(self.order)==0 and len(self.order_way)!=0:
            print("Please input sorting keyword!")
            print("\nBoth upper or lower case are accepted!")
        elif len(self.order)!=0 and len(self.order_way)==0:
            print("Please input sorting way including : 'asc' or 'dsec' !")
            print("\nBoth upper or lower case are accepted!")
        elif len(self.order)!=0 and len(self.order_way)!=0:
            print("\nOpen Database Successfully !\n")
            code_list = self.split_code()
            dayprice = pd.DataFrame()
            for code in code_list:
                condi = self.get_w_condi_list()
                w_condi = self.get_w_condi_str()
                fields = ['LAST_TRADE_DAY', 'TRADE_CODE']+condi
                conn = sq3.connect(path+str(indexcode[0:6]+'data.db'))
                c = conn.cursor()
                cursor = c.execute("SELECT " + w_condi + " from stockdata where LAST_TRADE_DAY Between '"+self.start_date+"' and '"+self.end_date+"' AND TRADE_CODE='"+code+"'"+" AND "+scon[0].upper()+scon[1]+scon[2]+" order by "+self.order.upper()+" "+self.order_way)
                tmp=cursor.fetchall()
                tmp_tmp = []
                for tup in tmp:  #元组转列表
                    tmp_tmp.append(list(tup))
                dict_index = []
                for g in tmp_tmp:#取字典的键
                    dict_index.append(g[0])
                dict = {}
                for o in range(0,len(dict_index)):#组成字典
                    dict[dict_index[o]] = tmp_tmp[o]
                dlist=list(dict.keys())
                fm = pd.DataFrame(dict,index = fields,columns = dlist)
            dayprice = dayprice.append(fm.T,ignore_index=True)
            print(dayprice)

    def get_detail(self):
        """根据con判断返回结果"""
        if len(self.con)==0:
            self.get_detail_nullcon()
        elif len(self.con)!=0:
            self.get_detail_con()
            
    def get_traday(self):
        """根据给出的起始日期和终止日期，返回数据库中交易日列表"""
        list_tmp = self.trade_dayt()
        dat_int = []
        i = list_tmp.index(self.start_trade_day())
        j = list_tmp.index(self.end_trade_day())
        for t in range(i,j+1):
            dat_int.append(list_tmp[t][0:10])
        print("\nThe trade day(s) between "+self.start_date[0:10]+" and "+self.end_date[0:10]+" is(are) :\n")
        print(dat_int)
        return dat_int
    
    def cal_traday(self):
        """根据给定的起始日期和终止日期，返回相隔的交易日数量"""
        list_tmp = self.trade_dayt()
        i = list_tmp.index(self.start_trade_day())
        j = list_tmp.index(self.end_trade_day())
        cal_trad = j-i+1
        print("\nThe amount of trade days between "+self.start_date[0:10]+" and "+self.end_date[0:10]+" is :",cal_trad)
            
