#-*- coding=utf-8 -*-
from flask import Flask, render_template, abort, send_from_directory, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import pymysql  # ImportError: No module named 'MySQLdb
import os
from flask_session import Session

pymysql.install_as_MySQLdb()
app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
app.config.from_object('settings')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@10.10.10.24:3306/consolemg?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 2
db = SQLAlchemy(app)  # 实例化db对象

app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='10.10.10.24', port=6379,db=6)
Session(app)

@app.route('/redis')
def hello_world():
    session['aa']='lis'
    print(session.get('aa'))
    return 'ok'

@app.before_request
def before():
    url = request.path
    pass_list = ['/login','/logout', '/chpasswd','/register']
    if url in pass_list or url.endswith('js') or url.endswith('.css') or \
            url.endswith('.png') or url.endswith('.jpg') or url.endswith('.ico'):
        pass
    elif session.get('islogin') != 'true':
        return redirect('/login')


@app.route('/aaa')
def aaaa():
    return render_template('overview.html')


# 接口测试
@app.after_request
def foot_log(environ):
    print("访问接口--->",request.path)
    return environ


if __name__ == '__main__':
    from application.index import *
    app.register_blueprint(index)
    from application.user import *
    app.register_blueprint(user)
    from application.link import *
    app.register_blueprint(link)

    app.run(debug=app.config['DEBUG'])

