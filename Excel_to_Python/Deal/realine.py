# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:16:13 2017

@author: jinjianfei
"""

#from WindPy import w
#w.start()

#import numpy as np
#import pandas as pd
import datetime
#from pandas.io import sql
#import sqlite3 as sq3
from datetime import datetime, date, time, timedelta
import re
import xlwings as xw


path = 'C:/Users/jinjianfei/Desktop/data/'
desktop = 'C:/Users/jinjianfei/Desktop/'
#filename = '2017年03月23日周四.txt'
filename = [#'国际信用.txt',
            #'国际利率.txt',
            #'国利信用.txt',
            #'国利利率.txt',
            #'平安信用.txt',
            #'平安利率.txt',
            #'信唐成交.txt',
            #'BGC利率.txt',
            #'BGC信用.txt'
            #'2017年03月23日周四.txt',
            '2017年09月13日周三.txt'
            ]    #在tab_judge（）时使用
date_fmt = "%Y-%m-%d"
start_date = datetime.strftime(datetime.today(),date_fmt)
#end_date = "2017-08-13"


class Deal():
    """"""
    
    def __init__(self):
        """"""
        
    def get_code(self):
        """"""
        for i in range(0,len(filename)):
            with open(path+filename[i]) as file_object:
                for line in file_object:
                    split_line_list = line.split('\t')
                    for i in split_line_list:
                        if re.match(r'^\d{9}|^\d{8}|^\d{7}$|^\d{6}|^\d{6}\.[SZ]|^\d{6}\.[SH]',i):
                            code = i
                            print(code)
                        
    def tab_judge(self):
        """判断.txt文件是否含有tab格"""
        for i in range(0,len(filename)):
            with open(path+filename[i]) as file_object:
                for line in file_object:
                    if "\t" in line:
                        print(filename[i] +" has tab")
                    else:
                        print(filename[i] +" has no tab")
                        
    def get_code_mod(self):
        """"""
        code_list = []
        for i in range(0,len(filename)):
            with open(path+filename[i]) as file_object:
                for line in file_object:  #遍历每行
                    split_line_list = line.split('\t')
                    for i in split_line_list:   #遍历每行元素
                        if re.match(r'^\d{9}',i):
                            code = i+'.IB'
                            code_list.append(code)
                        elif re.match(r'^\d{8}',i):
                            code = "0"+i+'.IB'
                            code_list.append(code)
                        elif re.match(r'^\d{7}',i):
                            code = i+'.IB'
                            code_list.append(code)
                        elif re.match(r'^\d{6}\.[SZ]',i):
                            code = i
                            code_list.append(code)
                        elif re.match(r'^\d{6}\.[SH]',i):
                            code = i
                            code_list.append(code)
                        elif re.match(r'^\d{6}',i):
                            code = i
                            if code[0:2] == '01' or code[0:3] == '122' or code[0:3] == '123' or code[0:3] == '124' or code[0:3] == '127' or code[0:3] == '139' or code[0:3] == '125' or code[0:3] == '136' or code[0:3] == '135' or code[0:3] == '131' or code[0:3] == '126':
                                code = code +'.SH'
                                code_list.append(code)
                            elif code[2:4] == '00' or code[2:4] == '01' or code[2:4] == '02' or code[2:4] == '03' or code[2:4] == '04' or code[2:4] == '99' or code[0:4] == '1606' or code[0:4] == '1689':
                                code = code +'.IB'
                                code_list.append(code)
                            elif code[0:3] == '109' or code[0:3] == '107' or code[0:3] == '111' or code[0:3] == '112' or code[0:3] == '117' or code[0:3] == '118' or code[0:3] == '116' or code[0:3] == '115' :
                                code = code +'.SZ'
                                code_list.append(code)
        code = []
        for i in code_list:
            code_tmp = []
            code_tmp.append(i)
            code.append(code_tmp)
#        print(code)
        return code
    
    def get_price(self):
        """测试有括号汉字失败"""
        price_list = []
        for i in range(0,len(filename)):
            with open(path+filename[i]) as file_object:
                for line in file_object:  #遍历每行
                    split_line_list = line.split('\t')
                    for i in split_line_list:   #遍历每行元素
                        if re.match(r'^\d{1}\.\d{2,4}$|^\d{1}\.\d{2}\%$|^\d$|^\d{1}\.\d{1}$',i):
                            #|^\d{1}\.\d{2}[行权]|^\d{1}\.\d{2}[(到期)]|^\d{1}\.\d{2}[(行权)]|^\d{1}\.\d{2}[到期]|
                            price = i
                            if '%' in price:
                                price = price[:-1]
                            else:
                                pass
                            print(price)
                            
    def get_price1(self):
        """可匹配1、2、3、4位价格小数，单独个位不能识别"""
        info = []
        for i in range(0,len(filename)):
            with open(desktop+filename[i]) as file_object:
                for line in file_object:  #遍历每行
                    split_line_list = line.split('\t')
                    line_list = []
                    for i in split_line_list:   #遍历每行元素
                        if not re.match(r'^\d.*[dDmMyY]$|^\d{2}[\u4e00-\u9fa5A-Z].*$|^[ABC].*\w$|^[A-Z].*|[\u4e00-\u9fa5a-z()：:（）+]+$|^\\{n}$|^\[]$|^\s$|^(0*)$|^[\u0020]$',i):
                            line_list.append(i)
                        else:
                            pass
                    if len(line_list)==0:
                        pass
                    elif len(line_list)==1:
                        line_list.append('')
                        info.append(line_list)
#                        print(line_list)
                    elif len(line_list)==2:
#                        print(line_list)
                        info.append(line_list)
                    
        print(info)
        return info         
                        
                        
                        
a=Deal()
#a.get_code_mod()
#a.get_price()
#a.get_price1()

app=xw.App(visible=True,add_book=False)
wb=app.books.add()
wb.save(desktop+start_date+".xlsx")
wb=app.books.open(desktop+start_date+".xlsx")
xw.sheets.add(name=start_date,before=None,after=None)
sht=wb.sheets[start_date]
sht.range('A1').value=['代码','价格','简称','评级','剩余期限','估值','估值偏离','前一日估值','估值变化','公司属性','债券类别','票面','上市日期','发行起始日','成交日期']
sht.range('A2').value=a.get_price1()
wb.save()
sht=wb.sheets[start_date]
rng=sht. range('A2').expand('down')
nrows = rng.rows.count
for i in range(0,nrows):
    sht.range('O'+str(i+2)).value= start_date    
wb.save()
wb.close()
app.quit()

































