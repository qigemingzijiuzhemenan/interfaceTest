#-*- coding:utf-8 -*-

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import readConfig as readConfig
from commons.Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, password, port, sender, title,build
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        build = localReadConfig.get_email("build")
        title = localReadConfig.get_email("subject")+build
        # self.content = localReadConfig.get_email("content")

        # get receiver list
        self.value = localReadConfig.get_email("receiver")
        self.receiver = []
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        # defined email subject
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = build+"接口测试报告" + " " + date

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')

    def config_header(self):
        """
        defined email header include subject, sender and receiver
        :return:
        """
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)

    def config_content(self):
        """
        write the content of email
        :return:
        """
        # htmls = '''<!DOCTYPE html>
        # <html>
        #  <head>
        #   <meta charset="UTF-8" />
        #  </head>
        #     <div class='heading'>
        #         <h1>holle！测试完成！以下是测试概况：</h1>
        #     <p class='attribute'><strong>测试环境:</strong> %s</p>
        #     <p class='attribute'><strong>开始时间:</strong> %s</p>
        #     <p class='attribute'><strong>耗时:</strong> %s</p>
        #     <p class='attribute'><strong>执行情况:</strong> %s</p>
        #     <br />
        #     <br />
        #     <br />
        #     <br />
        #         <h1>详细信息请查看附件。</h1>
        #     </div>
        # </html>'''
        # datas = [('开始时间', '2020-09-25 19:22:39'), ('耗时', '0:00:01.028517'), ('执行情况', '通过 3')]
        # testhj = '59.203.208.70'
        # content = htmls % (testhj, datas[0][1], datas[1][1], datas[2][1])
        f = open(os.path.join(readConfig.proDir,'testFile', 'emailStyle.html'),'rb')
        content = f.read()
        f.close()
        print(content)
        content_plain = MIMEText(content, 'html', 'UTF-8')
        # content_plain = MIMEText(self.content)
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        """
        config image that be used by content
        :return:
        """
        # defined image path
        image1_path = os.path.join(readConfig.proDir, 'testFile', 'img', '1.png')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        # self.msg.attach(msgImage1)
        fp1.close()

        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'logo.jpg')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        # self.msg.attach(msgImage2)
        fp2.close()

        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file
        :return:
        """

        # if the file content is not null, then config the email file
        if self.check_file():
            # build = localReadConfig.get_email("build")
            t=str(datetime.now().strftime("%Y%m%d%H%M%S"))
            reportpath = self.log.get_result_path()
            zippath = os.path.join(readConfig.proDir, "result", build+"testresult%s.zip"%t)

            # zip file
            files = glob.glob(reportpath + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结构
                f.write(file, '/report/'+os.path.basename(file))
            f.close()

            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="%stestresult%s.zip"'%(build,t)
            self.msg.attach(filehtml)

    def check_file(self):
        """
        check test report
        :return:
        """
        reportpath = self.log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def send_email(self):
        """
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("测试结果已通过电子邮件发送出去.")
        except Exception as ex:
            self.logger.error(str(ex))


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
    email.send_email()
