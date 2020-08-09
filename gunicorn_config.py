import logging, os, multiprocessing
import logging.handlers
from logging.handlers import WatchedFileHandler
'''
在项目目录里执行命令启动应用
gunicorn -c gunicorn_config.py main:app
'''
# 获取工作目录
BASE_DIR = os.path.abspath(os.curdir)
bind = '0.0.0.0:5000'
#进程数
workers = multiprocessing.cpu_count() * 2 + 1
#gunicorn要切换到的目的工作目录
chdir = BASE_DIR
# pid文件
pidfile = os.path.join(BASE_DIR, "flaskapp.pid")
#日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'debug'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 访问日志
accesslog = os.path.join(BASE_DIR, "access.log")
# 信息日志
errorlog = os.path.join(BASE_DIR, "error.log")