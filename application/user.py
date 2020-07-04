# -*- coding=utf-8 -*-
from flask import Blueprint, make_response, session, request, redirect, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import Users
import time
import re

from common.function import Caltime
user = Blueprint('user', __name__)


# 登录
## http: // 127.0.0.1:5000/login
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = Users()
        if request.headers.getlist("X-Forwarded-For"):
            ipaddr = request.headers.getlist("X-Forwarded-For")[0]  # 获取请求头部的IP ，用于nginx代理后获取用户的源ip
        else:
            ipaddr = request.remote_addr  # 获取请求ip地址
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        result = user.find_by_userinfo(username)
        result_u = user.find_by_username(username)
        if len(result_u) == 1:
            try:
                if check_password_hash(result['PASSWD'], password):
                    nowTime = Caltime(time.strftime('%Y-%m-%d'))
                    inactiveTime = result['INACTIVE']
                    if nowTime <= inactiveTime:
                        session['islogin'] = 'true'
                        session['userid'] = result['USERID']
                        session['username'] = result['USERNAME']
                        session['role'] = result['ROLE']
                        response = make_response('login-pass')
                        return response
                    elif inactiveTime == 0:
                        return 'For-the-first-time-login'
                    else:
                        return 'password-expired'
                else:
                    return 'login-error'
            except Exception as e:
                return 'error'
        else:
            return 'login-error'

# 注销登录
@user.route('/logout')
def logout():
    session.clear()
    response = make_response('注销登录并重定向', 302)
    response.headers['location'] = url_for('index.f_login')
    # 清空cookie，下面2条一样的效果，都是清空cookie
    response.delete_cookie('username')  # 删除cookie
    response.set_cookie('password', '', max_age=0)  # 设置cookie保存时间为0，即马上过期，效果和删除一样
    return response  # 返回到index.red函数,即index视图的red函数


# 用户注册
@user.route('/register', methods=['POST'])
def register():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    if len(password) < 5:
        return 'passwd-invalid'
    elif len(Users().find_by_username(username)) > 0:
        return 'user-repeated'
    else:
        userid = int(round(time.time() * 1000000))
        passwd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        Users().user_register(userid, username, passwd)
    return 'reg-pass'


# 修改密码
@user.route('/chpasswd', methods=['POST'])
def chpasswd():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    result = Users().find_by_username(username)
    # 密码包含数字，大小写字母，特殊字符 <>~!@#$%^&*()_+`-=[]{};'",./? 且长度不小于8位
    if len(password) < 8 or re.match("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[<~!@#$%^&*()_+`\-\=\[\]{};\'\",./?>])).*$",password) == None:
        return 'password-invalid'
    elif not len(result) > 0:
        return 'password-register'
    else:
        passwd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        Users().change_passwd(result[0].USERID, passwd)
    return 'change-password-pass'
