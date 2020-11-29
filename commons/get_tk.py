#-*- coding:utf-8 -*-
from commons import configHttp
from commons import update_urltomd5
import readConfig as readConfig
import requests
import time
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()

def get_token_app():
    pass

#获取pda的token
def get_token_pda():
    url='system/data'
    appId=localReadConfig.get_pda_data('appId')
    password=localReadConfig.get_pda_data('password')
    terminalno=localReadConfig.get_pda_data('terminalno')
    username=localReadConfig.get_pda_data('username')
    localConfigHttp.set_url(url)
    date='appId=%s&' \
         'method=preLogin&' \
         'module=pda&' \
         'password=%s&' \
         'service=Std&' \
         'terminalno=%s&' \
         'username=%s&' \
         've=2'%(appId,password,terminalno,username)
    new_url=localConfigHttp.url+"?"+update_urltomd5.url_to_md5(date)
    r=requests.get(new_url).json()
    token={'v':r['v'],
           'u':r['u']}
    # print(token)
    return token
# get_token_pda()