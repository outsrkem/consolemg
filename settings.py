#全局通用配置类
# class Config(object):
# config.py
#-*- coding=utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 调试模式
DEBUG = True

# 应用端口号
PORT = 8000

# host
HOST = '10.10.10.1'

# 用于session ID
SECRET_KEY = 'wderqeyJ2Y29kZSI6ImxkbG4ifQ.Xr-Lbg.ojkAcx7BZx7590luvEIvhYASA_8'

# 数据库连接信息
DB_HOSTIP = os.environ['DB_HOSTIP']
DB_PORT = os.environ['DB_PORT']
DB_DATABASE = os.environ['DB_DATABASE']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']


