import readConfig as readConfig
import unittest
import paramunittest
from commons.Log import MyLog
from commons import configHttp
from commons import common
from commons import DB_config_Oracle

Case_xls = common.get_xls("governCase.xlsx", "queryFxddFptj")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localConfigDB = DB_config_Oracle.DB()


@paramunittest.parametrized(*Case_xls)
class testqueryFxddFptj(unittest.TestCase):

    def setParameters(self, case_name, method, cookie, data, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param token:
        :param data:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.cookie = str(cookie)
        self.data = str(data)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
    def testqueryFxddFptj(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('queryFxddFptj')
        localConfigHttp.set_url(self.url)

        # set header
        if self.cookie == '0':
            cookie = localReadConfig.get_headers("fxdd_cookies")
            header = {"Content-Type": "application/json;charset=UTF-8",
                      "Cookie": cookie}
        elif self.cookie == '1':
            # cookie = None
            header = {"Content-Type": "application/json;charset=UTF-8"}
        localConfigHttp.set_headers(header)

        # set params
        # data = {'jsonStr': self.data}
        # localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.get()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['message'])

    def checkResult(self):
        """

        :return:
        """
        self.info = self.response.json()
        common.show_return_msg(self.response)
        if self.case_name =='queryFxddFptj':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['data']['fptj'], self.msg)


        if self.result == '1':
            pass
            # self.assertEqual(self.info['code'], self.code)
            # self.assertEqual(self.info['message'], self.msg)
            # if self.case_name == 'registerQuick_EmailExist':
            #     sql = common.get_sql('newsitetest', 'rs_member', 'delete_user')
            #     localConfigDB.executeSQL(sql, self.email)
            #     localConfigDB.closeDB()
if __name__ == '__main__':
    unittest.main()