# -*- coding=utf-8 -*-
from flask import Blueprint, make_response, session, request, redirect, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import Users
from common.redisdb import redis_connent
from common.function import generate_token, certify_token
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
        result_p = user.find_by_passwdinfo(username)
        result_u = user.find_by_userinfo(username)
        if len(result_u) == 1:
            try:
                if check_password_hash(result_p.PASSWD, password):
                    nowTime = Caltime(time.strftime('%Y-%m-%d'))
                    inactiveTime = result_p.INACTIVE
                    if nowTime <= inactiveTime:
                        session['islogin'] = 'true'
                        session['userid'] = result_u[0].USERID
                        session['username'] = result_u[0].USERNAME
                        session['role'] = result_u[0].ROLE
                        response = make_response('login-pass')
                        return response
                    elif inactiveTime == 0:
                        red = redis_connent()  # 连接redis 服务器
                        # 生成 token
                        token = generate_token(result_u[0].USERID, '1800')
                        # 保存一个token k:v 用户id：token
                        red.set(result_u[0].USERID, token)
                        red.expire(result_u[0].USERID, 2000)
                        return 'For-the-first-time-login'
                    else:
                        return 'password-expired'
                else:
                    return 'login-error'
            except Exception as e:
                return ("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))

        else:
            return 'login-error'


# 注销登录
@user.route('/logout')
def logout():
    session.clear()
    response = make_response('注销登录并重定向', 302)
    response.headers['location'] = url_for('index.f_login')
    return response  # 返回到index.red函数,即index视图的red函数


# 用户注册
@user.route('/register', methods=['POST'])
def register():
    '''
    @Args:
        username : 用户名
            1. 大写字母
            2. 小写字母
            3. 数字和大写字母或数字和小写字母
            4. @和数字或@和大写字母或@小写字母
                正则 re.match 需要优化，其他字符会成功 asdfg--
        password ：密码
    '''
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    if len(username) < 5 or re.match("^(?:(?=.*[A-Z])|(?=.*[a-z])|(?=.*[0-9])(?=.*[A-Z])|(?=.*[a-z])|(?=.*[@])(?=.*[0-9])|(?=.*[A-Z])|(?=.*[a-z])).*$", username) == None:
        return 'username-invalid'
    elif len(password) < 5:
        return 'passwd-invalid'
    elif len(Users().find_by_userinfo(username)) > 0:
        return 'user-repeated'
    else:
        userid = int(round(time.time() * 1000000))
        passwd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        row = Users().user_register(userid, username, passwd)
        if row == 'inst-pass':
            return 'reg-pass'
        elif row == 'inst-failed':
            return 'reg-failed'
    print(username)
    return 'error'


@user.route('/chpasswd', methods=['POST'])
def chpasswd():
    '''
    修改密码
    @Args:
        username : 用户名
        password ：密码
    @Return:
        返回修改结果
    需使用token认证用户是否输入过密码，且原密码认证通过
    '''
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    result = Users().find_by_userinfo(username)
    red = redis_connent()  # 连接redis 服务器
    session_userid = session.get('userid')
    # 用户是否存在
    if not len(result) > 0:
        return 'password-register'
    # 密码包含数字，大小写字母，特殊字符 <>~!@#$%^&*()_+`-=[]{};'",./? 且长度不小于8位
    elif len(password) < 8 or re.match("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[<~!@#$%^&*()_+`\-\=\[\]{};\'\",./?>])).*$", password) == None:
        return 'password-invalid'
    elif session_userid != None:  # 用户已登陆
        if session_userid == result[0].USERID:
            # 生成 token
            token = generate_token(result[0].USERID, '1800')
        else:
            return 'SystemException session_userid != result[0].USERID'
    else:
        token = red.get(result[0].USERID)

    # 修改密码开始
    try:
        if token != None:
            if certify_token(result[0].USERID, token):
                passwd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                Users().change_passwd(result[0].USERID, passwd)
            else:
                return 'error'
            return 'change-password-pass'
        else:
            return 'auth-failure'
    except Exception as e:
        print("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_lineno, e.__traceback__.tb_frame.f_globals['__file__'], e))
        return 'error'
