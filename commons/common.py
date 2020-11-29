import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from commons import configHttp as configHttp
from commons.Log import MyLog as Log
from commons import DB_config_Mysql,DB_config_Oracle,get_md5date
import json
import time
from commons.Log import MyLog
from commons import Get_excel

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()
caseNo = 0

def get_pda_token():
    appid = localReadConfig.get_pda_date("appId")
    comid=localReadConfig.get_pda_date("comid")
    terminalno = localReadConfig.get_pda_date("terminalno")
    username = localReadConfig.get_pda_date("uasename")
    userPwd = localReadConfig.get_pda_date("password")
    ip = localReadConfig.get_http('baseurl')
    prot = localReadConfig.get_http('port')
    ip = f'http://{ip}:{prot}/system/data?'
    url = f'appId={appid}&' \
        f'comid={comid}&' \
        f'method=preLogin&' \
        f'module=pda&' \
        f'password={userPwd}&' \
        f'pdaareatype=1&' \
        f'service=Std&' \
        f'terminalno={terminalno}&' \
        f'username={username}&' \
        f've=2'
    url_new = get_md5date.get_kq_app(url)
    r = requests.get(ip+url_new)
    token = {'u': r.json()['u'], 'v': r.json()['v'],'sings':str(r.json()['signstate'])}
    logger.debug("Create token:%s" % (token))

    return token

#时间转时间戳
def get_times(date):
    dt = date
    #转换成时间数组
    timeArray = time.strptime(dt, "%Y/%m/%d %H:%M:%S")#:%S
    #转换成时间戳
    timestamp = int(time.mktime(timeArray))*1000
    return timestamp

#时间戳转时间
def get_date_times(date):
    timeArray = time.localtime(int(date)/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def get_app_token():
    appid=localReadConfig.get_app_date("appId")
    comid=localReadConfig.get_app_date("comid")
    ts=str(round(time.time() * 1000))
    userPhoneNum=localReadConfig.get_app_date("uasename")
    userPwd=localReadConfig.get_app_date("password")
    ip=localReadConfig.get_http('baseurl')
    prot=localReadConfig.get_http('port')
    ip=f'http://{ip}:{prot}/system/data?'
    url=f'appId={appid}' \
        f'&comid={comid}' \
        '&method=appLogin' \
        f'&module=app' \
        '&service=Std' \
        f'&ts={ts}' \
        '&u=' \
        f'&userPhoneNum={userPhoneNum}' \
        f'&userPwd={userPwd}' \
        '&v=&ve=2&'
    url_new=get_md5date.get_kq_app(url)
    r=requests.get(ip+url_new)
    # print(r.text)
    token={'u':r.json()['u'],'v':r.json()['v']}
    logger.debug("Create token:%s" % (token))

    return token

#更新config.ini里的app和pda的token
def set_token_to_config(types=None):
    """
    set token that created for visitor to config
    :return:
    """
    if types=='app':
        token = get_app_token()
        localReadConfig.set_headers("token_v_app", token['v'])
        localReadConfig.set_headers("token_u_app", token['u'])
    if types=='pda':
        token = get_pda_token()
        localReadConfig.set_headers("token_v_pda", token['v'])
        localReadConfig.set_headers("token_u_pda", token['u'])
        localReadConfig.set_pda("qdtype", token['sings'])
    if types=='web':
        pass

def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['data']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    # 可以显示中文
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
# ****************************** read testCase excel ********************************

#paramunittest方式的数据源读取（excel）
def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls
#ddt方式的数据源读取（excel）
def get_xlsx(filepach, sheet):
    data=Get_excel.read_casefile_2(filepach, sheet)
    return data

#新建Excel
def create_Excel(path):
    New_Excel=Get_excel.New_xlsx(path)
    return New_Excel

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text[17:-13]
                table[table_name] = sql
            database[db_name] = table

def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    # print(url_list)
    url = '/'.join(url_list)
    return url

def ConfigHttp():
    localConfigHttp = configHttp.ConfigHttp()
    return localConfigHttp


def DB_Mysql():
    DB_mysql=DB_config_Mysql.MyDB_new()
    return DB_mysql


def DB_Oracle():
    DB_Oracle=DB_config_Oracle.DB()
    return DB_Oracle


def my_log():
    my_log=MyLog.get_log()
    return my_log

if __name__ == "__main__":
    print("common")
    a=get_xls("governCase.xlsx", "queryFxddFptj")
    print(a)
    # sql = get_sql('tlcn', 'gzsj', 'tj_gzsj')
    # print(sql.format('无照经营'))
    # tj = db.select_data(sql.format('无照经营'))
    # print(tj)

    # print(get_xls("gzfxCase.xlsx","getgzsjlist"))
    # print(get_xls("userCase.xlsx", "login"))
    # set_visitor_token_to_config()#获取token
    # c=get_url_from_xml('login')
    # a=get_url_from_xml('getgzsjlist')
    # print(a)
    # data={"code":"0000","message":"请求成功","data":{"total":1,"size":10,"pages":1,"current":1,"records":[{"qtbmTxt":"市城管执法局","gzmc":"无照经营游商","qtbm":"34070020000000000001","id":"5fe7ce2a1b30465d9ca18cacdfd80385","bh":"20200807151805","gzdm":"19","fxdd":"铜官区_东郊办事处_开源社区_铜都大道三岔路口","ztTxt":"","fxsj":"2020-08-07 15:18:05"}]}}
    # bh=get_value_from_return_json(data, 'records', 0)['bh']
    # print(bh)