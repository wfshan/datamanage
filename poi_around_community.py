# --gaode-周边poi检索
import requests
import shapely.geometry as SG
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt,degrees,atan2
#计算两点距离
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000

#计算多变行中心点
def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))

def str2list(s):
    x = s[2:-2].split('], [')
    l = []
    for i in x:
        c = i.split(',')
        cc = [float(c[0]),float(c[1])]
        l.append(cc)
    return l

def mean_distance(cent,poly):
    poly = str2list(poly)
    l = []
    for i in poly:
        d = haversine(cent[0],cent[1],i[0],i[1])
        l.append(d)
    return sum(l)/len(l)




#获取住宅坐标

#餐饮服务  050000

#小区中心点和平均距离
fence = pd.read_csv('e:/desktop/vanke/vanke社区地理围栏(上海+合肥).csv',engine='python')
fence['comm_center'] = fence['gd_fence'].apply(lambda x:center_geolocation(str2list(x)))
fence['distance'] = fence.apply(lambda x:mean_distance(x['comm_center'],x['gd_fence']),axis=1)


#poi爬取
types = '050000'
url = 'https://restapi.amap.com/v3/place/around?'
location = str(round(fence['comm_center'][0][0],6))+','+str(round(fence['comm_center'][0][1],6))
key = '413746af7157e65ad9657b127e9932f2'
keywords = '醉湘居(徐泾店)'#fence['community'][0]
#city = '310000'
radius = str(int(1000+fence['distance'][0]))
extensions = 'base'
offset = '20'
page = '1'
para = 'key='+key+'&location='+location+'&types='+types+'&radius='+radius+'&offset='+offset+'&page='+page+'&extensions='+extensions 
items = requests.get(url+para)
lis = items.json()



def get_page(types,location,radius,page):
    url = 'https://restapi.amap.com/v3/place/around?'
    key = '413746af7157e65ad9657b127e9932f2'
    offset = '20'
    para = 'key='+key+'&location='+location+'&types='+types+'&radius='+radius+'&offset='+offset+'&page='+str(page)+'&extensions='+extensions 
    items = requests.get(url+para)
    lis = items.json()
    contents = []
    for item in lis['pois']:
        content = [item['id'],item['name'],item['type'],item['typecode'],item['address'],item['location'],item['distance']]
        contents.append(content)
    return contents

#500
resul = pd.DataFrame()
for n in fence['community']:
    fence2 = fence[fence['community']==n]
    location = str(round(fence2['comm_center'].values[0][0],6))+','+str(round(fence2['comm_center'].values[0][1],6))
    radius = str(int(500+fence2['distance'].values[0]))
    co = []
    for ty in ['050000','080000','150000','141200','090000','060000']:
        types=ty
        for i in range(1,100):
            page = i
            print(n,types,i)
            newco = get_page(types,location,radius,page)
            co = co+newco
            if len(newco)==0:
                break
    c = pd.DataFrame(co)
    c.columns = ['id','name','type','typecode','address','location','distance']
    c['community'] = n
    resul = pd.concat([resul,c])

#resul = resul.drop_duplicates()           
#resul.to_excel('e:/desktop/vanke/community1000_poi.xlsx',index=False) 
resul.to_excel('e:/desktop/vanke/community500_poi.xlsx',index=False) 
