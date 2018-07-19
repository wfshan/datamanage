import math

def computearea(pointlist):
    """
    给定某区域高德地图边界坐标，计算该区域面积
    """
    arr = pointlist
    arr_len = len(arr)
    if arr_len < 3:
        return 0.0
    temp = arr
    s = temp[0][1] * (temp[arr_len -1][0]-temp[1][0])
    for i in range(1,arr_len):
        s += temp[i][1] * (temp[i-1][0] - temp[(i+1)%arr_len][0])
    return round(math.fabs(s/2)*9101160000.085981,6)
