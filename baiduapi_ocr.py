# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 17:56:09 2019

@author: wfsha
"""

from aip import AipNlp

APP_ID = '15375342'
API_KEY = '9jh0LZyVCWVO2b88Dg6u9e7E'
SECRET_KEY = '2tRnYDWqX03y8ZGQr1C09MvZTyGnp0di'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = ""
client.lexer(text)


from aip import AipOcr

APP_ID = '15375464'
API_KEY = 'gmDvtiMls4tx6Gj4nIy1Y0KQ'
SECRET_KEY = 'cZQp6X8dWalxW5KU7hWG61zcoig0Z8Ak'    

filePath = 'e:/desktop/timg1.jpg'
def ocr(filePath):
    image = open(filePath, 'rb').read()
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    res = client.basicGeneral(image)
    return res['words_result']
