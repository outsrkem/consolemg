#全局通用配置类
# class Config(object):
# config.py
#-*- coding=utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class logconfig():
    # 设置日志文件，和字符编码
    logging.basicConfig(level=logging.INFO)
    # 创建日志记录器，　指明日志保存的路径、每个日志的大小、保存日志的上限
    file_log_handler = RotatingFileHandler('consolemg.log', maxBytes=1024 * 1024, backupCount=10)
    # 设置日志的格式       日志等级       日志信息的文件名　　行数　　日志信息
    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
    # 将日志记录器指定日志的格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

# 调试模式

DEBUG = True

# 应用端口号
PORT = 8000

# host
HOST = '10.10.10.1'

# 用于session ID
SECRET_KEY = 'wderqeyJ2Y29kZSI6ImxkbG4ifQ.Xr-Lbg.ojkAcx7BZx7590luvEIvhYASA_8'

# 用于获取根路径


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



