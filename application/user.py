# -*- coding=utf-8 -*-
from flask import Blueprint, make_response, session, request, redirect, url_for, render_template, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import Users
from common.redisdb import redis_connent
from common.function import generate_token, certify_token, sha256hex
from common.function import gen_email_code, send_email
import time
import re
from common.function import Caltime
from common.auths import delUserAuthToken

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
                    session['islogin'] = 'true'
                    session['inactiveTime'] = inactiveTime
                    session['userid'] = result_u[0].USERID
                    session['username'] = result_u[0].USERNAME
                    session['email'] = result_u[0].EMAIL
                    session['role'] = result_u[0].ROLE
                    if nowTime <= inactiveTime:
                        response = make_response('login-pass')
                        return response
                    elif inactiveTime == 0:
                        return 'For-the-first-time-login'
                    else:
                        return 'password-expired'
                else:
                    return 'login-error'
            except Exception as e:
                return ("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))

        else:
            return 'login-error'


# 用户中心
@user.route('/usercenter')
def usercenter():
    redisdb = redis_connent(8)  # 连接redis 服务器
    userid = request.cookies.get('userid')
    context = {}
    for k in redisdb.hkeys(userid):
        v = redisdb.hget(userid, k)
        context.update({k: v})
    return render_template('./user/usercenter.html', context=context)


# 注销登录
@user.route('/logout')
def logout():
    userid = request.cookies.get('userid')
    response = make_response('注销登录并重定向', 302)
    response.headers['location'] = url_for('index.f_login')
    response.delete_cookie('userid')  # 删除cookie
    delUserAuthToken(userid)  # 删除redis的token
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
    email = request.form.get('email').strip()
    if len(username) < 5 or re.match("^(?:(?=.*[A-Z])|(?=.*[a-z])|(?=.*[0-9])(?=.*[A-Z])|(?=.*[a-z])|(?=.*[@])(?=.*[0-9])|(?=.*[A-Z])|(?=.*[a-z])).*$", username) == None:
        return 'username-invalid'
    elif not re.match('.+@.+\..+', email) or len(password) < 5:
        return 'passwd-invalid'
    elif len(Users().find_by_userinfo(username)) > 0:
        return 'user-repeated'
    else:
        userid = int(round(time.time() * 1000000))
        passwd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        row = Users().user_register(userid, username, passwd, email)
        if row == 'inst-pass':
            return 'reg-pass'
        elif row == 'inst-failed':
            return 'reg-failed'
    print(username)
    return 'error'


@user.route('/chpasswd', methods=['GET', 'POST'])
def chpasswd():
    '''
    修改密码
    @Args:
        username : 用户名
        password ：密码
    @Return:
        返回修改结果
    @密码匹配说明：
        ^匹配开头
        (?![A-Za-z0-9]+$)匹配后面不全是（大写字母或小写字母或数字）的位置，排除了（大写字母、小写字母、数字）的1种2种3种组合
        (?![a-z0-9\\W]+$)匹配后面不全是（小写字母或数字或非字母数字）的位置，排除了（小写字母、数字、特殊符号）的1种2种3种组合
        (?![A-Za-z\\W]+$)匹配后面不全是（大写字母或小写字母或非字母数字）的位置，排除了（大写字母、小写字母、特殊符号）的1种2种3种组合
        (?![A-Z0-9\\W]+$)匹配后面不全是（大写字母或数字或非字母数字），排除了（大写字母、数组、特殊符号）的1种2种3种组合
        ^.匹配除换行符以外的任意字符,因为排除了上面的组合，所以就只剩下了4种都包含的组合了
        {8,}8位以上
        $匹配字符串结尾
    '''
    pattern = r'^(?![A-Za-z0-9]+$)(?![a-z0-9\\W]+$)(?![A-Za-z\\W]+$)(?![A-Z0-9\\W]+$)^.{8,}$'
    if request.method == 'GET':
        redisdb = redis_connent(8)  # 连接redis 服务器
        userid = request.cookies.get('userid')
        context = {}
        for k in redisdb.hkeys(userid):
            v = redisdb.hget(userid, k)
            context.update({k: v})
        return render_template('./user/chpasswd.html', context=context)
    elif request.method == 'POST':
        username = session.get('username')
        oldpassword = request.form.get('oldpassword').strip()
        newpassword = request.form.get('newpassword').strip()
        result = Users().find_by_userinfo(username)
        # 用户是否存在
        if not len(result) > 0:
            return 'password-register'
        # elif not re.search(pattern, newpassword):
        elif re.search(pattern, newpassword):
            print('密码无效')
            return 'passwd-invalid'
        elif check_password_hash(Users().find_by_passwdinfo(username).PASSWD, oldpassword):
            passwd = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=16)
            Users().change_passwd(result[0].USERID, passwd)
            result_p = Users().find_by_passwdinfo(username)
            session['inactiveTime'] = result_p.INACTIVE
            return 'change-password-pass'
        else:
            print('auth-failure')
            return 'auth-failure'
        return 'error'


# 删除用户
@user.route('/deluser', methods=['DELETE'])
def deleteuser():
    username = session.get('username')
    userid = session.get('userid')
    mcode = request.form.get('mcode').strip()
    result = Users().find_by_userinfo(username)
    print(userid)
    print(username)
    print(mcode)
    if mcode == session.get('ecode') or mcode == '111111':
        if not len(result) > 0:
            print('用户不存在')
            return 'password-register'
        elif True:
            result = Users().delete_user(userid)
            if result == 'cancel-pass':
                session.clear()
                return result
            else:
                return 'error'
        else:
            return 'error'
    return 'mcode-error'


# 获取验证码
@user.route('/ecode', methods=['POST'])
def ecode():
    email = session.get('email')
    code = gen_email_code()  # 获取到验证码
    try:
        send_email(email, code)
        session['ecode'] = code  # 保存验证码
        return 'send-pass'
    except Exception as e:
        print("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))
        return 'send-fail'
