# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 09:32:33 2017

@author: jinjianfei
"""

import re

"""测试正则表达式"""

#test = ['4.45行权','5.23到期','5.00行权（散量）','5.23（到期）','5.23(行权)','5.23（行权）','5.23(行权)三两','5.23']
test = ['','\n','\t']
test = ['5','5.0','5.01','5.011','5.0111']
for i in test:
#    if re.match(r'^\d{1}\.\d{2}$|^\d{1}\.\d{2}\([\u4E00-\u9FA5]+\)$|^\d{1}\.\d{2}[\u4E00-\u9FA5]+$', i):
#    if not re.match(r'^\d.*[dDmMyY]$|^\d{2}[\u4e00-\u9fa5A-Z].*$|^[ABC].*\w$|^\s$',i):    
    if not re.match(r'^\d.*[dDmMyY]$|^\d{2}[\u4e00-\u9fa5A-Z].*$|^[ABC].*\w$|^[A-Z].*|[\u4e00-\u9fa5a-z()：:（）+]+$|^\\{n}$|^\[]$|^\s$|^(0*)$|^[\s\S]$',i):
        print(i)
    else:
        print('failed')
    
    
#m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
#m

# m.group(0)
#'010-12345'
#>>> m.group(1)
#'010'
#>>> m.group(2)
#'12345'