import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from commons import configHttp as configHttp
from commons.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()
from commons import DB_config_Oracle
caseNo = 0
db=DB_config_Oracle.DB()

def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


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

if __name__ == "__main__":
    print("common")
    # sql = get_sql('tlcn', 'gzsj', 'tj_gzsj')
    # print(sql.format('无照经营'))
    # tj = db.select_data(sql.format('无照经营'))
    # print(tj)

    print(get_xls("gzfxCase.xlsx","getgzsjlist"))
    # print(get_xls("userCase.xlsx", "login"))
    # set_visitor_token_to_config()#获取token
    # c=get_url_from_xml('login')
    a=get_url_from_xml('start_parking_pda')
    print(a)
    # data={"code":"0000","message":"请求成功","data":{"total":1,"size":10,"pages":1,"current":1,"records":[{"qtbmTxt":"市城管执法局","gzmc":"无照经营游商","qtbm":"34070020000000000001","id":"5fe7ce2a1b30465d9ca18cacdfd80385","bh":"20200807151805","gzdm":"19","fxdd":"铜官区_东郊办事处_开源社区_铜都大道三岔路口","ztTxt":"","fxsj":"2020-08-07 15:18:05"}]}}
    # bh=get_value_from_return_json(data, 'records', 0)['bh']
    # print(bh)