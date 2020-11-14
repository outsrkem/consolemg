# 全局通用配置类
# class Config(object):
# config.py
# -*- coding=utf-8 -*-
import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ReadConfig():
    yamlPath = os.path.join(BASE_DIR, 'consolemg.yaml')
    f = open(yamlPath, 'r', encoding='utf-8')
    x = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    return x


# 优先获取环境变量
def TestConfiguration(key):
    x = ReadConfig()
    config = os.environ.get(key, False)
    if config:
        return config
    else:
        # print("warning: There are no environment variables " + key)
        return x[key.split("_")[0]][key.split("_")[1]]


# 调试模式
DEBUG = True
# 应用端口号
PORT = 8000

# host
HOST = '10.10.10.25'


APP_HOST = TestConfiguration("APP_HOST")
APP_PORT = TestConfiguration("APP_PORT")
APP_DEBUG = TestConfiguration("APP_DEBUG")



# 用于session ID
SECRET_KEY = 'wderqeyJ2Y29kZSI6ImxkbG4ifQ.Xr-Lbg.ojkAcx7BZx7590luvEIvhYASA_8'

# 数据库连接信息
DB_HOSTIP = TestConfiguration("DB_HOSTIP")
DB_PORT = TestConfiguration("DB_PORT")
DB_DATABASE = TestConfiguration("DB_DATABASE")
DB_USERNAME = TestConfiguration("DB_USERNAME")
DB_PASSWORD = TestConfiguration("DB_PASSWORD")