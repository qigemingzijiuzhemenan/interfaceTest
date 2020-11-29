import cx_Oracle
import os
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
class DB():
    #连接数据库
    def __init__(self,username=None,password=None,host=None,port=None,sid=None):
        #Oracle的参数
        if host !=None:
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.sid = sid
        else:
            root_path = os.path.abspath(os.path.dirname(__file__)).split('test_run')[0]#获取当前项目的所在路径
            # print(root_path)
            self.username = localReadConfig.get_Or_db("username")
            self.password = localReadConfig.get_Or_db("password")
            self.host = localReadConfig.get_Or_db("host")
            self.port = localReadConfig.get_Or_db("port")
            self.sid = localReadConfig.get_Or_db("db_name")
        self.dsn = cx_Oracle.makedsn(self.host,self.port,self.sid)

    # 创建连接对象
    def __connect_databases(self):
        try:
            # 创建连接
            self.conn = cx_Oracle.connect(self.username,self.password,self.dsn)
            cursor = self.conn.cursor()  # 创建游标
            return cursor
        except cx_Oracle.Error as Error:
            print("数据库连接失败：%s" % (Error))
    #字典的key全部转化为小写
    def capital_to_lower(self,dict_info):
        new_dict = {}
        for i, j in dict_info.items():
            new_dict[i.lower()] = j
        return new_dict
    #解析查询的数据
    def analysis_data(self,name,values):
        try:
            data = []
            num = 0
            while num < len(values):
                num_1 = 0
                c = {}
                while num_1 < len(name):
                    c[name[num_1][0]] = values[num][num_1]
                    num_1 += 1
                data.append(self.capital_to_lower(c))
                # print(d)
                num += 1
        except Exception as Error:
                return Error
        return data
        #查询数据
    def select_data(self,SQL):
        try:
            cursor = self.__connect_databases()     #建立游标
            cursor.execute(SQL)      #在游标上使用SQL语句
            name = cursor.description
            values = cursor.fetchall()    #返回所有数据
            # row = cursor.fetchone()  #返回一行数据
            # row = cursor.fetchmany(2)#返回两行数据
            if len(values)>0:
                data=self.analysis_data(name, values)
                return data
            else:
                return None
        except cx_Oracle.Error as Error:
            print("查询出错：%s" % (Error))
        finally:  # 无论怎样都会执行下面的关闭连接数据库的代码
            self.conn.close()
    #插入/更新数据
    def inster_data(self, SQL):
        try:
            cursor = self.__connect_databases()  # 建立游标
            cursor.execute(SQL)  # 在游标上使用SQL语句
            num=cursor.rowcount
            # name = cursor.description
            # values = cursor.fetchall()  # 返回所有数据
            # row = cursor.fetchone()  #返回一行数据
            # row = cursor.fetchmany(2)#返回两行数据
            self.conn.commit()
            # print(SQL)
            print("受影响%d行"%num)
        except cx_Oracle.Error as Error:
            print("插入出错：%s" % (Error))
        finally:  # 无论怎样都会执行下面的关闭连接数据库的代码
            cursor.close()
            self.conn.close()

    #删除数据
    def delete_data(self, SQL):
        try:
            cursor = self.__connect_databases()  # 建立游标
            cursor.execute(SQL)  # 在游标上使用SQL语句
            num = cursor.rowcount
            # name = cursor.description
            # values = cursor.fetchall()  # 返回所有数据
            # row = cursor.fetchone()  #返回一行数据
            # row = cursor.fetchmany(2)#返回两行数据
            self.conn.commit()
            # print(SQL)
            print("受影响%d行" % num)
        except cx_Oracle.Error as Error:
            print("插入出错：%s" % (Error))
        finally:  # 无论怎样都会执行下面的关闭连接数据库的代码
            cursor.close()
            self.conn.close()



#测试此模块
# username = "u_tl_cscn_test"  # 生产：U_TL_CSCN测试：u_tl_cscn_test
# password = "w9rmvCNrOfjZ"  # 生产Cxcd2qgRQfsN：测试：w9rmvCNrOfjZ
# host = "59.203.208.53"  # 生产：59.203.208.52，测试：59.203.208.53
# port = "1521"
# sid = "testcnywdb"  # 生产：cnywdb测试：testcnywdb
# db = DB()
# id='8dbe2dbfc7e34e54b5d296120da70000'
# sql = '''SELECT count(*) 总数 FROM T_GZFX_GZSJ_JCXX gzsj
# LEFT JOIN T_GZFX_PZ_CJPZ jc ON GZSJ.CJLX=JC.GZDM
# WHERE GZMC LIKE'%无照经营%'
# '''
# data = db.select_data(sql)
# print(data)
# print(type(data))



