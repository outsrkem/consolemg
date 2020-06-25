#-*- coding=utf-8 -*-
from flask import Flask, render_template, abort, send_from_directory, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import pymysql  # ImportError: No module named 'MySQLdb
pymysql.install_as_MySQLdb()
app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
app.config.from_object('settings')
app.config['SECRET_KEY'] = 'wderqeyJ2Y29kZSI6ImxkbG4ifQ.Xr-Lbg.ojkAcx7BZx7590luvEIvhYASA_8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@10.10.10.24:3306/consolemg?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 实例化db对象


if __name__ == '__main__':
    from application.user import *
    app.register_blueprint(user)
    app.run(debug=app.config['DEBUG'])

