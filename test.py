#-*- coding:utf-8 -*-
import paramunittest
import unittest
import ddt
import random
from commons import common,Get_excel
from commons import DB_config_Oracle
import requests
from xml.sax import saxutils
# Case_xls = Get_excel.read_casefile_2("Billingrules.xlsx", "Billingrules")
# case=[['querynumber', 'post', '0', '{"current":1,"bh":"20200807151805","size":10}', '0', '0000', '20200807151805'], ['querytype', 'post', '0', '{"current":1,"gzmc":"无照经营","qtbm":"","size":10}', '0', '0000', '无照经营游商']]

# 冒泡排序
def bubble_sort(arr):
    length = len(arr)
    for i in range(0,length-1):
        for j in range(0,length-i-1):
            if arr[j]>arr[j+1]:
                t = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = t
def get_random_list(n):
    l = []
    for i in range(0,n):
        l.append(random.randint(1,10))
    return l


def get_data(data):
    for i in range(1,len(data)):
        for k in range(len(data)-i):
            if data[k]>data[k+1]:
                a=data[k]
                data[k]=data[k+1]
                data[k + 1]=a
li = get_random_list(10)
print(li)
get_data(li)
print(li)
# for i in range(1,len(li)):
#     for j in range(len(li) - i):
#         if li[j] > li[j + 1]:
#             temp = li[j]
#             li[j] = li[j + 1]
#             li[j + 1] = temp
# print(li)

#
# a='1'
# b='2'
# c=b and a
# print('%(b)s,%(a)s'%dict(a=a,
#                          b=b))


# @paramunittest.parametrized(*case)
# class testlist(unittest.TestCase):
#     def setParameters(self, a, b, c, d, e, f, g):
#         self.a=a
#         self.b=b
#         self.c=c
#         self.d=d
#         self.e=e
#         self.f=f
#         self.g=g
#
#     def test_list(self):
#         print(self.a,self.b,self.d,self.d,self.e,self.f,self.g)
#     def tearDown(self):
#         """
#
#         :return:
#         """
#         pass


# @ddt.ddt
# class testlist(unittest.TestCase):
#     @ddt.data(*Case_xls)
#     # @ddt.unpack
#     def setdate(self,data):
#         self.case_name = data['case_name']
#         self.berthcode = data['case_name']
#         self.vehicletype = data['vehicletype']
#         self.carproperty = data['carpropertycarproperty']
#         self.dotime = data['dotimedotime']
#         self.endtime = data['endtime']
#         self.msg = data['message']
#         self.response = None
#         self.info = None
#     def setUp(self):
#         self.setdate()
#     def test_list(self):
#         print(self.case_name)
# if __name__ == '__main__':
#     unittest.main()