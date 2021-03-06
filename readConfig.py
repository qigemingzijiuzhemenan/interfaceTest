# -*- coding: utf-8 -*-
import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
    def set_pda(self, name, value):
        self.cf.set("PDA", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_My_db(self, name):
        value = self.cf.get("Mysql_DATABASE", name)
        return value
    def get_Or_db(self, name):
        value = self.cf.get("oracle_DATABASE", name)
        return value
    def get_Sql_db(self, name):
        value = self.cf.get("sqlserver_DATABASE", name)
        return value
    def get_app_date(self, name):
        value = self.cf.get("APP", name)
        return value
    def get_pda_date(self, name):
        value = self.cf.get("PDA", name)
        return value

