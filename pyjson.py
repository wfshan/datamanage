# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 09:27:55 2018

@author: wfsha
"""

import pandas as pd
import re

import os

filedir = 'E:/Desktop/xian/allslides/7403.txt'
def to_df(filedir):
    f = open('%s'%filedir,'r').read()
    def spli(s):
        return s.split(',') 
    f2 = ''.join(f.split('[[')[1].split('"'))[:-3]
    f3 = f2.split('],[')
    n1 = f.split('[[')[0].split('},{')    
    name = []
    for i in n1:
        r = re.findall(r'name":"(.*)","type',i)
        k = r[0].split('.')
        if len(k)>1:name.append(r[0].split('.')[1])
        else:name.append(r[0].split('.')[0])             
    f4 = pd.DataFrame(list(map(spli,f3)),columns=name)
    return f4
to_df(filedir).to_csv(filedir+'aa.csv')


filedir = 'E:/Desktop/tt/'
def co_df(filedir):
    t = pd.DataFrame()
    for i in os.listdir(filedir):
        f = to_df(filedir+'%s'%i)
        t = pd.concat([t,f],axis=0)
    return t

co_df(filedir).to_csv(filedir+'aa.csv')
