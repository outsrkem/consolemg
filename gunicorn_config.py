import logging, os, multiprocessing
import logging.handlers
from logging.handlers import WatchedFileHandler
'''
在项目目录里执行命令启动应用
gunicorn -c gunicorn_config.py main:app
'''

# 获取工作目录
BASE_DIR = os.path.abspath(os.curdir)
LOG_DIR = os.path.join(BASE_DIR, "log")

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


bind = '0.0.0.0:443'

# 代码更新时将重启工作，默认为False。此设置用于开发，每当应用程序发生更改时，都会导致工作重新启动。
reload = True

# 设置守护进程
#daemon = True

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
accesslog = os.path.join(LOG_DIR, "access.log")
# 信息日志
errorlog = os.path.join(LOG_DIR, "error.log")

# https
# certfile=os.path.join(BASE_DIR, "cert", "www.pem")
# keyfile=os.path.join(BASE_DIR, "cert", "www-key.pem")