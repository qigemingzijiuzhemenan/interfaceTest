# -*- coding:utf-8 -*-
import paramunittest
import unittest
import ddt
import random
from commons import common, Get_excel
from commons import DB_config_Oracle
import requests
from xml.sax import saxutils

# Case_xls = Get_excel.read_casefile_2("Billingrules.xlsx", "Billingrules")
# case=[['querynumber', 'post', '0', '{"current":1,"bh":"20200807151805","size":10}', '0', '0000', '20200807151805'], ['querytype', 'post', '0', '{"current":1,"gzmc":"无照经营","qtbm":"","size":10}', '0', '0000', '无照经营游商']]


Case_xls = common.get_xls("gzfxCase.xlsx", "getgzsjlist")


@paramunittest.parametrized(*Case_xls)
class testlist(unittest.TestCase):
    def setParameters(self, a, b, c, d, e, f, g):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')

    def setUp(self) -> None:
        print('setUp')

    def test_1(self):
        print('test_1')
        print(self.a, self.b, self.d, self.d, self.e, self.f, self.g)

    def test_2(self):
        print('test_2')
        print(self.a, self.b, self.d, self.d, self.e, self.f, self.g)

    def tearDown(self) -> None:
        print('tearDown')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass')


# Case_xls = Get_excel.read_casefile_2("gzfxCase.xlsx", "getgzsjlist")
# @ddt.ddt
# class testlist(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         print('setUpClass')
#
#     def setUp(self) -> None:
#         print('setUp')
#     @ddt.data(*Case_xls)
#     # @ddt.unpack
#     def test_1(self,data):
#         print('test_1')
#         print(data)
#         self.case_name = data['case_name']
#         self.berthcode = data['method']
#         self.vehicletype = data['cookie']
#         self.carproperty = data['data']
#         self.dotime = data['result']
#         self.endtime = data['code']
#         self.msg = data['msg']
#
#     def test_2(self):
#         print('test_2')
#     def tearDown(self) -> None:
#         print('tearDown')
#
#     @classmethod
#     def tearDownClass(cls) -> None:
#         print('tearDownClass')
if __name__ == '__main__':
    unittest.main()
