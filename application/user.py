#-*- coding=utf-8 -*-
from flask import Blueprint, make_response, session, request, redirect, url_for,render_template
from models.users import Users
import hashlib
import re
import base64
user = Blueprint('user', __name__)


#登录
## http: // 127.0.0.1:5000/login
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user = Users()
        if request.headers.getlist("X-Forwarded-For"):
            ipaddr = request.headers.getlist("X-Forwarded-For")[0]  #获取请求头部的IP ，用于nginx代理后获取用户的源ip
        else:
            ipaddr = request.remote_addr  # 获取请求ip地址
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        # 实现登录
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and user.find_passwd(result[0].USERID)[0].PASSWD==password:
            session['islogin'] = 'true'
            session['userid'] = result[0].USERID
            session['username'] = username
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=30*24*3600)
            response.set_cookie('password', password, max_age=30*24*3600)
            return response
        else:
            return 'login-error'

# 注销登录
@user.route('/logout')
def logout():
    session.clear()
    response = make_response('注销登录并重定向', 302)
    response.headers['location'] = url_for('user.login')
    # 清空cookie，下面2条一样的效果，都是清空cookie
    response.delete_cookie('username')  # 删除cookie
    response.set_cookie('password', '',max_age=0)  # 设置cookie保存时间为0，即马上过期，效果和删除一样
    return response  # 返回到index.red函数,即index视图的red函数
