#-*- coding:utf-8 -*-
import pymysql
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
class MyDB_new():
    #连接数据库
    def __init__(self,username=None,password=None,host=None,port=None,dbname=None):
        #MySQL的参数
        if host !=None:
            self.host = host
            self.port = port
            self.user = username
            self.password = password
            self.database = dbname
        else:
            self.host = localReadConfig.get_My_db("host")
            self.port = int(localReadConfig.get_My_db("port"))
            self.user = localReadConfig.get_My_db("username")
            self.password = localReadConfig.get_My_db("password")
            self.database = localReadConfig.get_My_db("database")

    # 创建连接和游标
    def __connect_databases(self):
        try:
            # 创建连接
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        port=self.port,
                                        password=self.password,
                                        database=self.database,
                                        charset='utf8')
            # 创建游标
            cursor = self.conn.cursor()
            return cursor
        except pymysql.Error as Error:
            print("数据库连接失败：%s" % (Error))

    # 字典的key全部转化为小写
    def capital_to_lower(self, dict_info):
        new_dict = {}
        for i, j in dict_info.items():
            new_dict[i.lower()] = j
        return new_dict

    # 解析查询的数据
    def analysis_data(self, name, values):
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
            values = cursor.fetchall()  # 返回所有数据
            # row = cursor.fetchone()  #返回一行数据
            # row = cursor.fetchmany(2)#返回两行数据
            data =self.analysis_data(name,values)
            return data
        except pymysql.Error as Error:
            print("查询出错：%s" % (Error))
        finally:  # 无论怎样都会执行下面的关闭连接数据库的代码
            self.conn.close()

    # 插入数据
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
            print(SQL)
            print("受影响%d行"%num)
        except pymysql.Error as Error:
            print("插入出错：%s" % (Error))
        finally:  # 无论怎样都会执行下面的关闭连接数据库的代码
            cursor.close()
            self.conn.close()

#测试此模块

db = MyDB_new()
sql = 'select * from db;'

data = db.select_data(sql)
for b in data:
    print(b)
