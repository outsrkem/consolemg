# -*- coding=utf-8 -*-
from flask import Blueprint, request, jsonify, make_response
from common.redisdb import redis_connent
from common.auths import authenticate
from common.utility import trueReturn, falseReturn


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def authlogin():
    """
    用户登录认
    @param   username:
    @param   password
    @return  json
    """
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    print("登录的用户名和密码：",username,password)
    result = authenticate(username, password)
    if result.get_json()['status']:
        usertoken = result.get_json()['data']['token']
        userid = result.get_json()['data']['userid']
        response = make_response(result) # 使用make_response设置响应头部
        response.headers['X-Auth-Token'] = usertoken
        response.set_cookie('userid', userid, max_age=30 * 24 * 3600)
        return response
    else:
        return result




from common.auths import identify, decode_auth_token
@auth.route('/user', methods=['GET'])
def authuser():
    """
    获取用户信息，校验token测试
    @param   X-Auth-Token 头部信息，用户token
    @return  json
    @Examples
        curl -i -k -H "Content-Type:application/json" \
        -H "X-Auth-Token:$AUTHTOKEN" \
        -X GET https://10.10.10.1:5000/auth/user
    """
    result = identify(request)
    if (result['status'] and result['data']):
        redisdb = redis_connent()  # 连接redis 服务器
        user = {}
        userid = result['data']
        for k in redisdb.hkeys(userid):
            v = redisdb.hget(userid, k)
            user.update({k: v})

        returnUser = {
            'id': user['userid'],
            'username': user['username'],
            'email': user['email'],
            'login_time': user['login_time']
        }
        result = trueReturn(returnUser, "请求成功", "200")
    return jsonify(result)