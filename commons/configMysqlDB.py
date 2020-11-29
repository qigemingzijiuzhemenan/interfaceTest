import pymysql
import readConfig as readConfig
from commons.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

#Mysql
class MyDB:
    global host, username, password, port, database, config
    host = localReadConfig.get_My_db("host")
    username = localReadConfig.get_My_db("username")
    password = localReadConfig.get_My_db("password")
    port = localReadConfig.get_My_db("port")
    database = localReadConfig.get_My_db("database")
    config = {
        'host': str(host),
        'user': username,
        'passwd': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None
        # print(config)

    def connectDB(self):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def executeSQL(self, sql, params):
        """
        execute sql
        :param sql:
        :return:
        """
        self.connectDB()
        # executing sql
        self.cursor.execute(sql, params)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        # print(value)
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("Database closed!")
