# -*- coding: utf-8 -*-
import hashlib

#md5加密
def md5value(date):
    # print(date)
    input_name = hashlib.md5()
    input_name.update(date.encode("utf-8"))
    # return (input_name.hexdigest()).upper()#大写的32位
    # return (input_name.hexdigest())[8:-8].upper()#"大写的16位"
    return  (input_name.hexdigest()).lower()#"小写的32位"
    # return  (input_name.hexdigest())[8:-8].lower()#"小写的16位"

#给请求地址补充md5加密
def get_kq_app(url):
    keys='&requestKey=0388c639da8e703e3549e372e280b37e'
    u=url+keys
    sign="sign="+md5value(u)
    new_url=url+'&'+sign
    return new_url

# ip='http://192.168.9.101:6085/system/data?'
# url1='appId=083533342&comid=200000042&endparktime=1605571440000&isescape=0&method=overParking&module=pda&orderid=20201126172659660859592105120309&outareaid=20180313100409687466755474319009&outcantonid=320301&outsectionid=20180913190834542795545981729288&payType=1&pdaareatype=1&service=Std&terminalno=864316030002542&u=20201109171423491112262105679684&v=20201126172659577885212374584508&ve=2'
# url3='appId=083533342&comid=200000042&endparktime=1605571440000&issensor=0&method=overParking&module=pda&orderid=20201126172659660859592105120309&outareaid=20180313100409687466755474319009&outcantonid=320301&outsectionid=20180913190834542795545981729288&payType=1&pdaareatype=1&service=Std&terminalno=864316030002542&u=20201109171423491112262105679684&v=20201126172659577885212374584508&ve=2'
# print(get_kq_app(url1))
# print(get_kq_app(url3))