# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 17:56:09 2019

@author: wfsha
"""

import requests
import string
import time
import hashlib
import json
import pandas as pd
 
#init
api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
my_appid = '20190108000255405'
cyber = '4WceeMIv3wchsIdEXslD'

def translate(from_,to_,word):
    salt = str(time.time())[:10]
    final_sign = str(my_appid)+word+salt+cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    paramas = {
        'q':str(word),
        'from':str(from_),
        'to':str(to_),
        'appid':'%s'%my_appid,
        'salt':'%s'%salt,
        'sign':'%s'%final_sign
        }
    response = requests.get(api_url,params = paramas).content
    content = str(response,encoding = "utf-8")
    json_reads = json.loads(content)
    return json_reads['trans_result'][0]['dst']

translate('zh','en','床前明月光')


语言简写	名称
auto	自动检测
zh	中文
en	英语
yue	粤语
wyw	文言文
jp	日语
kor	韩语
fra	法语
spa	西班牙语
th	泰语
ara	阿拉伯语
ru	俄语
pt	葡萄牙语
de	德语
it	意大利语
el	希腊语
nl	荷兰语
pl	波兰语
bul	保加利亚语
est	爱沙尼亚语
dan	丹麦语
fin	芬兰语
cs	捷克语
rom	罗马尼亚语
slo	斯洛文尼亚语
swe	瑞典语
hu	匈牙利语
cht	繁体中文
vie	越南语
