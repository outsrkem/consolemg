#全局通用配置类
# class Config(object):
# config.py
#-*- coding=utf-8 -*-
import os
# 调试模式

DEBUG = True

# 应用端口号
PORT = 8000

# host
HOST = '127.0.0.1'

# 用于session ID
SECRET_KEY = 'wderqeyJ2Y29kZSI6ImxkbG4ifQ.Xr-Lbg.ojkAcx7BZx7590luvEIvhYASA_8'

# 用于获取根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义数据库连接信息
def loginfo():
    DB_USERNAME = 'blognote'
    DB_PASSWORD = '123456'
    try:
        DB_HOSTIP = os.environ['DB_HOSTIP']
    except Exception:
        DB_HOSTIP = '10.10.10.24'
    DB_PORT = '3306'
    DB_DATABASE = 'blognote'
    # print('数据库连接信息---> {用户名:%s,密码:%s,数据库IP:%s,数据库端口:：%s,数据库名称:%s}' % (DB_USERNAME , DB_PASSWORD,DB_HOSTIP,DB_PORT,DB_DATABASE))
    return DB_USERNAME, DB_PASSWORD, DB_HOSTIP, DB_PORT, DB_DATABASE
DB_INFO = loginfo()



