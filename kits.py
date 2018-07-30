# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:05:37 2018

@author: wfsha
"""


'''
1、根据边界坐标估算该区域大致面积
input：区域的边界坐标
output：该区域的估算面积
'''
import math

def computearea(pointlist):
    arr = pointlist
    arr_len = len(arr)
    if arr_len < 3:
        return 0.0
    s = arr[0][1] * (arr[arr_len -1][0]-arr[1][0])
    for i in range(1,arr_len):
        s += arr[i][1] * (arr[i-1][0] - arr[(i+1)%arr_len][0])
    return round(math.fabs(s/2)*10000,3)


'''
2、坐标转换
input：原坐标，转换前后的坐标类别函数
output：转换后的坐标
'''
from coordTransform_utils import wgs84_to_bd09
import pandas as pd

result1 = wgs84_to_bd09(116.469271,39.985568)

df = pd.read_csv('E:/Desktop/workf/shdistrict.csv',encoding='utf8')
newlist = pd.DataFrame(list(map(wgs84_to_bd09,df['lon'],df['lat'])))

df['bdlat'] = newlist[1]
df['bdlon'] = newlist[0]



'''
3、画简易热力图
input：有坐标点和该点权重组成的数据集
output：能反应坐标及热点（不明显）分布情况的热量力图
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('E:/Desktop/heatmap.csv')
df.columns = ['id','lon','lat','gender','age','prov_id','w','n']
p2 = df[['lon','lat','w']]
p3 = p2.pivot_table(index = 'lon',columns = 'lat',values = 'w',aggfunc=[np.sum])
plt.pcolormesh(p3,cmap=plt.cm.Paired)


'''
4、判断一个点是否在某给定区域内
input：所需判断的点的坐标，以及区域的边界坐标
output：点在该区域内则返回1，正在区域外则返回0
'''
import shapely.geometry as SG
from shapely.geometry import Point

def isinpoly(poly,lat,lng):
    if  SG.Polygon(poly).contains(Point(lat,lng)):
        return 1
    else:
        return 0

    #poly:多边形边界坐标，要求按顺时针或逆时针顺序排列
    #lat\lng:所要判断的点的坐标，坐标前后顺序跟poly中一致
    
    
df = pd.read_json('E:/Desktop/decathlon/drivetime.json')
df.columns = ['lng','lat']

#获取所要判断的点列
mapdf = pd.read_csv('E:/Desktop/workf/slide/sli.csv')
mapdf.columns = ['id','date','ptype','city','lat','lng','local','gender','age','n']
poly = list(zip(df['lng'],df['lat']))


mapdf['isin'] = np.array
mapdf['isin'] = mapdf.apply(lambda x:isinpoly(poly,x.lng,x.lat),axis = 1)

mapdf.to_csv('C:/Users/wfsha/Desktop/drivemap2.csv')
    
    
'''
5、生成可用于网页热力图的json文件
input：包含lon,lat,weight的dataframe
output：符合格式的json文件
'''

import pandas as pd
import numpy as np
import json
df2 = pd.read_csv('E:/desktop/decathlon/drivemap3.csv')

df3 = df[['count','lat','lng']]
df3 = df3.groupby(['lat','lng'])[['count']].sum()
df3 = df3.reset_index()
df3 = df3[['count','lat','lng']]
v = df3.T.to_dict().values()
with open('E:/Desktop/test.json','w') as f:
    f.write('{"dataArray":')
    f.write(json.dumps(list(v)))
    f.write('}')


'''
6、获取某地区边界坐标(高德)
input：地区名,如'上海'(加引号)
output：该地区在高德地图上的边界坐标及其相关信息
'''
import urllib
import numpy as np
import json
import pandas as pd 
from urllib.parse import quote

def getlnglat(address):
    address = quote(address)
    url = 'http://restapi.amap.com/v3/config/district?'
    #高德上申请的key
    key = '413746af7157e65ad9657b127e9932f2'
    uri = url + 'keywords=' + address +  '&key=' + key + '&subdistrict=1' + '&extensions=all'
    #uri = 'http://restapi.amap.com/v3/config/district?keywords=上海&key=413746af7157e65ad9657b127e9932f2&subdistrict=1&extensions=all'
    #访问链接后，api会回传给一个json格式的数据
    temp = urllib.request.urlopen(uri)
    temp = json.loads(temp.read())    
    #polyline是坐标，name是区域的名字    
    Data = temp["districts"][0]['polyline']
    name = temp["districts"][0]['name']
    citycode = temp["districts"][0]['citycode']
    adcode = temp["districts"][0]['adcode']
    #polyline数据是一整个纯文本数据，不同的地理块按照|分，块里面的地理信息按照；分，横纵坐标按照，分，因此要对文本进行三次处理
    Data_Div1 = Data.split('|')  #对结果进行第一次切割，按照|符号
    len_Div1 = len(Data_Div1)  #求得第一次切割长度 
    
    num = 0
    len_Div2 = 0   #求得第二次切割长度，也即整个数据的总长度
    while num < len_Div1 :
        len_Div2 += len(Data_Div1[num].split(';'))
        num += 1
    
    num = 0   
    num_base = 0
    output = np.zeros((len_Div2,5)).astype(np.float)   #循环2次，分割；与，        
    while num < len_Div1 :
        temp = Data_Div1[num].split(';')
        len_temp = len(temp)
        num_temp = 0
        while num_temp < len_temp:
            output[num_temp+num_base,:2] = np.array(temp[num_temp].split(','))#得到横纵坐标
            output[num_temp+num_base,2] = num_temp + 1#得到横纵坐标的连接顺序
            output[num_temp+num_base,3] = num + 1#得到块的序号
            num_temp += 1
        num_base += len_temp
        num += 1      
    
    output = pd.DataFrame(output,columns=['lng','lat','orderlist','block','name'])
    output['name'] = name
    output['citycode'] = citycode
    output['adcode'] = adcode
    
    return output

'''
7、获取某一点X分钟车程的范围边界坐标
input：坐标点，时间（单位分钟）
output：边界坐标
'''
import urllib
import json
'''
lng：坐标经度
lat：坐标维度
t：车程时间，单位分钟
'''
def drivingarea(lng,lat,t):
    url = 'http://geohey.com/s/routing/drivetime?loc=[' + str(lng) + ',' + str(lat) + ']&time=' + str(t) + '&ak=NGE3NWNkODk5N2U4NDZmNzgxYmFjNTM4MjdmMTI3MDE'
    temp = urllib.request.urlopen(url)
    temp = json.loads(temp.read())    
    a = temp['data'][0]   
    return a

'''
8、批量重复性Sql
input：语句的重复部分，以及需要规律变换部分
output：以txt格式存储的语句，可直接复制使用
'''
import pandas as pd

with open('E:/Desktop/queue.txt','wb') as f:
    for i in range(1,58):
        s = 'select t.date, t.ptype, t.city,t.lat,t.lon,t.local, t.gender, t.age,t.n from temp_lc_20180718_jn6 t where t.slides = %d;\n'%i
        f.write(s.encode())
###########
casedf = pd.read_csv('C:/Users/wfsha/Desktop/spot_full_wgs.csv',encoding='gbk')
with open('E:/Desktop/case.txt','wb') as f:
    for i in range(len(casedf['lon'])):
        s = 'when f.lon = '+ str(casedf['lon'][i])+ ' and f.lat = '+str(casedf['lat'][i])+' then '+str(casedf['spot'][i])+'\n'
        f.write(s.encode())

'''
9、
'''



