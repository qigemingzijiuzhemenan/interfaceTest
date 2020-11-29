#-*- coding:utf-8 -*-
import hashlib



#请求加上sign值
def url_to_md5(url):
    key='requestKey=0388c639da8e703e3549e372e280b37e'
    date=url+"&"+key
    input_name = hashlib.md5()
    input_name.update(date.encode("utf-8"))
    # (input_name.hexdigest()).upper()#"大写的32位"
    # (input_name.hexdigest())[8:-8].upper()#"大写的16位"
    sign="&sign=%s"%(input_name.hexdigest()).lower()#"小写的32位"
    # (input_name.hexdigest())[8:-8].lower()#"小写的16位"
    return url+sign

# a='appId=083533342&berthcode=300001&carplatecolour=1&carproperty=1&comid=200000042&dotime=1605916800000&issensor=1&method=startParking&module=pda&payType=1&pdaareatype=1&platenumber=粤V60001&sectionid=20180913190834542795545981729288&service=Std&terminalno=A100004A9C46FB&u=20201109171423491112262105679684&v=20201122004617678192976110350466&ve=2&vehicletype=1'
# b='appId=083533342&berthcode=300001&carplatecolour=1&carproperty=1&comid=200000042&dotime=1605916800000&issensor=1&method=startParking&module=pda&payType=1&pdaareatype=1&platenumber=粤V60001&sectionid=20180913190834542795545981729288&service=Std&terminalno=A100004A9C46FB&u=20201109171423491112262105679684&v=20201122005129860710969928192426&ve=2&vehicletype=1'
# print(url_to_md5(a))
# print(url_to_md5(b))