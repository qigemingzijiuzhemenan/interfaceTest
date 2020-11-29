# -*- coding: utf-8 -*-
import readConfig as readConfig
import unittest
import paramunittest
from commons.Log import MyLog
from commons import common,get_md5date
import time

Case_xls = common.get_xls("Billing_rulesCase.xlsx", "Billing_rules")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = common.ConfigHttp()
localConfigDB = common.DB_Mysql()


@paramunittest.parametrized(*Case_xls)
class testBilling_rules(unittest.TestCase):

    def setParameters(self, case_name, method, carnumber, berthcode, vehicletype, carproperty, startime,endtime,pay,message):
        """
        set parameters

        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.carnumber = str(carnumber)
        self.berthcode = str(berthcode)
        self.vehicletype ='1' if vehicletype =='工作日' else vehicletype =='非工作日' '2'
        self.carproperty ='1' if carproperty =='小型车' else carproperty =='大型车' '2'
        self.startime=common.get_times(str(startime))
        self.endtime=common.get_times(str(endtime))
        self.pay=str(pay)
        self.msg = str(message)
        self.response = None
        self.info_Start = None

    def description(self):
        """
        :return:
        """
        self.case_name

    #PDA申请停车
    def setUp(self):
        """

        :return:
        """
        self.token=common.get_pda_token()
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        url = common.get_url_from_xml('parking')

        # set token to config

        # set params
        params = f"appId={localReadConfig.get_pda_date('appId')}&" \
            f"berthcode={self.berthcode}&" \
            f"carplatecolour=1&" \
            f"carproperty={self.carproperty}&" \
            f"comid={localReadConfig.get_pda_date('comid')}&" \
            f"dotime={self.startime}&" \
            f"issensor=1&" \
            f"method=startParking&" \
            f"module=pda&" \
            f"payType=1&" \
            f"pdaareatype=1&" \
            f"platenumber={self.carnumber}&" \
            f"sectionid={localReadConfig.get_pda_date('sectionid')}&" \
            f"service=Std&" \
            f"terminalno={localReadConfig.get_pda_date('terminalno')}&" \
            f"u={self.token['u']}&" \
            f"v={self.token['v']}&" \
            f"ve=2&" \
            f"vehicletype={self.vehicletype}"
        self.url = url + '?' + get_md5date.get_kq_app(params)
        localConfigHttp.set_url(self.url)

        # test interface
        self.response = localConfigHttp.get()

        # check result
        self.checkResult_Start()
        self.log.build_case_line(self.case_name, str(self.info_Start['_outTime']), self.info_Start['message'])
        self.orderid = self.response.json()['orderid']

    #PDA结束订单并检查金额
    def test_parking_Billing(self):
        """
        test body
        :return:
        """
        # set url
        url = common.get_url_from_xml('parking')

        # set token to config

        # set params
        params = f"appId={localReadConfig.get_pda_date('appId')}&" \
            f"comid={localReadConfig.get_pda_date('comid')}&" \
            f"endparktime={self.endtime}&" \
            f"isescape=0&" \
            f"method=overParking&" \
            f"module=pda&" \
            f"orderid={self.orderid}&" \
            f"outareaid={localReadConfig.get_pda_date('areaid')}&" \
            f"outcantonid={localReadConfig.get_pda_date('cantonid')}&" \
            f"outsectionid={localReadConfig.get_pda_date('sectionid')}&" \
            f"payType=1&" \
            f"pdaareatype=1&" \
            f"service=Std&" \
            f"terminalno={localReadConfig.get_pda_date('terminalno')}&" \
            f"u={self.token['u']}&" \
            f"v={self.token['v']}&" \
            f"ve=2"
        self.url = url + '?' + get_md5date.get_kq_app(params)
        localConfigHttp.set_url(self.url)

        # test interface
        self.response = localConfigHttp.get()

        # check result
        self.checkResult_End()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, str(self.info_Start['_outTime']), self.info_Start['message'])
        self.log.build_case_line(self.case_name, str(self.info_End['_outTime']), self.info_End['message'])

    def checkResult_Start(self):
        """
        :return:
        """
        self.info_Start = self.response.json()
        common.show_return_msg(self.response)
        self.assertEqual(self.info_Start['message'], self.msg)

    def checkResult_End(self):
        """
        :return:
        """
        self.info_End = self.response.json()
        common.show_return_msg(self.response)
        if self.assertEqual(self.info_End['message'], self.msg) is None: #断言结束订单的操作成功，才会进行金额判断
            sql = f'''SELECT actualpay FROM tra_road_order WHERE id={self.info_End['orderid']}'''
            amount=localConfigDB.select_data(sql)[0]['actualpay']
            self.assertEqual(int(amount), int(self.pay))
            self.log.Billing_case_line(self.case_name, str(amount), self.pay)

if __name__ == '__main__':
    testBilling_rules()