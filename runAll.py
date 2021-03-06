import os
import unittest
from commons.Log import MyLog as Log
import readConfig as readConfig
from commons import HTMLTestRunner_new
from commons.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()

class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")#测试脚本所在文件夹路径
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()
        self.build = localReadConfig.get_email("build")

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name)
            # self.caseFile = os.path.join(readConfig.proDir, "testCase\\%s\\"%filepath)  # 测试脚本所在文件夹路径
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            # print("添加%s"%discover)
            suite_module.append(discover)
        if len(suite_module) > 0:

            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********测试 开始********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner_new.HTMLTestRunner(stream=fp, title=self.build+'接口测试报告', description='本次测试已完成，以下是测试详情。')
                runner.run(suit)
            else:
                logger.info("没有要测试的用例.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********测试 结束*********")
            fp.close()
            # send test report by email
            if on_off == 'on':
                self.email.send_email(runner.data)
            elif on_off == 'off':
                logger.info("测试结果没有发送邮件.")
            else:
                logger.info("Unknow state.")

if __name__ == '__main__':
    obj = AllTest()
    obj.run()
