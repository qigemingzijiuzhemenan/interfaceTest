import requests
import readConfig as readConfig
from commons.Log import MyLog as Log
from commons import update_urltomd5
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url_1(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host+":%s"%port+"/"+update_urltomd5.url_to_md5(url)
        self.logger.info("Url设置成功：%s"%self.url)

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host+":%s"%port+"/"+url
        self.logger.info("Url设置成功：%s"%self.url)

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header
        self.logger.info("headers设置成功：%s"%self.headers)

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param
        self.logger.info("params设置成功：%s"%self.params)

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data
        self.logger.info("data设置成功：%s"%self.data)

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}
            self.logger.info("set_files设置成功：%s" % file_path)
            # self.logger.info("set_files设置成功：%s" % self.files)

        if filename == '' or filename is None:
            self.state = 1
            self.logger.info("files设置成功：没有文件" )
    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            self.logger.info("response获取成功：%s"%response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            self.logger.info("response获取成功：%s" % response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            self.logger.info("response_WithFile获取成功：%s" % response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            self.logger.info("response获取成功：%s" % response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    print("ConfigHTTP")
    c='tl-cyberbrain-govern/fxtj/queryFxddFptj'
    a=ConfigHttp()
    a.set_url(c)
    print(a.url)
    a.headers = {"Content-Type": "application/json;charset=UTF-8",
              "Cookie": 'JSESSIONID=EF29D8626A41CB2BBD6718E686B2C831'}
    # a.data={'jsonStr': '{"current":1,"gzmc":"无照经营","qtbm":"","size":10}'}
    print(a.get().text)
