import shapely.geometry as SG
from shapely.geometry import Point


def isinpoly(poly,lat,lng):
    """
    判断给定的坐标点是否在某一区域内
    poly:某区域边界坐标
    lat、lng:所要判断的坐标点
    """
    if  SG.Polygon(poly).contains(Point(lat,lng)):
        return True
    else:
        return False
 #样例       
 for i in range(len(dist['district'])):
    def isinpoly2(lat,lng):
        if  SG.Polygon(dist['blist'][i]).contains(Point(lat,lng)):
            return True
        else:
            return False
    df2['TorF'] = df2.apply(lambda x:isinpoly2(x.lat,x.lng),axis = 1)  
    df2['dist'][df2['TorF'] == True] = dist['district'][i]
    print(i)
