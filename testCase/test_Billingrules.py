import readConfig as readConfig
import unittest
import paramunittest
from commons.Log import MyLog
from commons import configHttp
from commons import common
from commons import DB_config_Oracle
from commons import get_tk

Case_xls = common.get_xls("Billingrules.xlsx", "Billingrules")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localConfigDB = DB_config_Oracle.DB()
token=get_tk.get_token_pda()

@paramunittest.parametrized(*Case_xls)
class test_Billingrules(unittest.TestCase):

    def setParameters(self, case_name, cartype, carnumber,berthcode, vehicletype, carproperty, startime, dotime,etime,endtime,pay,message):
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
        self.appId=localReadConfig.get_pda_data('appId')
        self.berthcode = str(berthcode)
        self.carnumber=str(carnumber)
        self.comid=localReadConfig.get_pda_data('comid')
        self.cartype = str(cartype)
        self.carproperty = str(carproperty)
        self.dotime = str(dotime)
        self.endtime = str(endtime)
        self.pay = str(pay)
        self.sectionid=localReadConfig.get_pda_data('sectionid')
        self.terminalno=localReadConfig.get_pda_data('terminalno')
        self.u,self.v=token['u'],token['v']
        self.vehicletype = str(vehicletype)
        self.message = str(message)
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
    def test_start_parking_pda(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('start_parking_pda')
        localConfigHttp.set_url_1(self.url%(self.appId,self.berthcode,self.carproperty,self.comid,self.dotime,self.carnumber,self.sectionid,self.terminalno,self.u,self.v,self.vehicletype))

        # set header
        # if self.cookie == '0':
        #     cookie = localReadConfig.get_headers("fxdd_cookies")
        #     header = {"Content-Type": "application/json;charset=UTF-8",
        #               "Cookie": cookie}
        # elif self.cookie == '1':
        #     # cookie = None
        #     header = {"Content-Type": "application/json;charset=UTF-8"}
        # localConfigHttp.set_headers(header)

        # set params
        # params = 'appId=%s&' \
        #        'berthcode=%s&' \
        #        'carproperty=%s&' \
        #        'comid=%s&' \
        #        'carplatecolour=1&' \
        #        'dotime=%s&' \
        #        'issensor=1&' \
        #        'method=startParking&' \
        #        'module=pda&' \
        #        'payType=1&' \
        #        'pdaareatype=1&' \
        #        'platenumber=%s&' \
        #        'sectionid=%s&' \
        #        'service=Std&' \
        #        'terminalno=%s&' \
        #        'u=%s&' \
        #        'vehicletype=%s&' \
        #        'v=%s&ve=2'%(self.appId,self.berthcode,self.carnumber,self.comid,self.dotime,self.carnumber,self.sectionid,self.terminalno,self.u,self.vehicletype,self.v)
        # param=self.url%(self.appId,self.berthcode,self.carnumber,self.comid,self.dotime,self.carnumber,self.sectionid,self.terminalno,self.u,self.vehicletype,self.v)
        # localConfigHttp.set_params(param)

        # test interface
        self.response = localConfigHttp.get()

        # check result
        self.checkResult()

    def test_end_parking(self):
        pass
        # """
        # test body
        # :return:
        # """
        # # set url
        # self.url = common.get_url_from_xml('test_Billingrules')
        # localConfigHttp.set_url(self.url)
        #
        # # set header
        # # if self.cookie == '0':
        # #     cookie = localReadConfig.get_headers("fxdd_cookies")
        # #     header = {"Content-Type": "application/json;charset=UTF-8",
        # #               "Cookie": cookie}
        # # elif self.cookie == '1':
        # #     # cookie = None
        # #     header = {"Content-Type": "application/json;charset=UTF-8"}
        # # localConfigHttp.set_headers(header)
        #
        # # set params
        # params = 'appId=%s&' \
        #        'berthcode=%s&' \
        #        'carproperty=%s&' \
        #        'comid=%s&' \
        #        'carplatecolour=1&' \
        #        'dotime=%s&' \
        #        'issensor=1&' \
        #        'method=startParking&' \
        #        'module=pda&' \
        #        'payType=1&' \
        #        'pdaareatype=1&' \
        #        'platenumber=%s&' \
        #        'sectionid=%s&' \
        #        'service=Std&' \
        #        'terminalno=%s&' \
        #        'u=%s&' \
        #        'vehicletype=%s&' \
        #        'v=%s&ve=2'%(self.appId,self.berthcode,self.carnumber,self.comid,self.dotime,self.carnumber,self.sectionid,self.terminalno,self.u,self.vehicletype,self.v)
        # localConfigHttp.set_params(params)
        #
        # # test interface
        # self.response = localConfigHttp.get()
        #
        # # check result
        # self.checkResult()

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
        self.assertEqual(self.info['message'], self.message)

if __name__ == '__main__':
    unittest.main()