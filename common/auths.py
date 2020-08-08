import jwt, datetime, time
from flask import jsonify
from models.users import Users
from common.utility import trueReturn, falseReturn
from werkzeug.security import check_password_hash
from common.redisdb import redis_connent
from base64 import b64encode, b64decode


def encode_auth_token(user_id, login_time):
    """
    生成认证Token
    :param user_id: int
    :param login_time: int(timestamp)
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': user_id,
                'login_time': login_time
            }
        }
        return jwt.encode(
            payload,
            "x7BZx7590luvEIvhYA",
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    验证Token
    :param auth_token:
    :return: integer|string
    """
    try:
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, "x7BZx7590luvEIvhYA", options={'verify_exp': False})
        if ("data" in payload and 'id' in payload['data']):
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'


def authenticate(username, password):
    """
    用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
    :param password:
    :return: json
    """
    result_p = Users().find_by_passwdinfo(username)
    result_u = Users().find_by_userinfo(username)
    if len(result_u) == 1:
        try:
            if check_password_hash(result_p.PASSWD, password):
                login_time = int(time.time())
                userid = result_u[0].USERID
                username = result_u[0].USERNAME
                email = result_u[0].EMAIL
                role = result_u[0].ROLE
                inactive = result_p.INACTIVE
                redisdb = redis_connent()  # 连接redis 服务器

                redisdb.hmset(userid, {'userid': userid, 'login_time': login_time, 'username': username, 'email': email,
                                       'role': role, 'inactive': inactive})
                token = encode_auth_token(userid, login_time)
                token = b64encode(token)

                redisdb.set("Token-" + userid, token)
                data = {
                    'token': token.decode(),
                    'userid': userid,
                    'username': username
                }
                result = trueReturn(data, '登录成功')

                return jsonify(result)
            else:
                return jsonify(falseReturn('', '密码不正确'))
        except Exception as e:
            return ("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))

    else:
        return jsonify(falseReturn('', '找不到用户'))


def identify(request):
    """
    用户鉴权
    :return: list
    """
    auth_header = request.headers.get('X-Auth-Token')
    userid = request.cookies.get('userid')
    print(auth_header)
    print(userid)
    if auth_header != "" or auth_header != None:
        auth_tokenArr = auth_header.split(" ")
        auth_token = auth_tokenArr[0]
    else:
        if userid is not None:
            redisdb = redis_connent()  # 连接redis 服务器
            auth_tokenArr = redisdb.get("Token-" + userid).split(" ")
            auth_token = auth_tokenArr[0]
        else:
            result = falseReturn('', '没有提供认证token')
            return result

    if auth_token:
        auth_token = b64decode(auth_token)
        payload = decode_auth_token(auth_token)
        if not isinstance(payload, str):
            redisdb = redis_connent()  # 连接redis 服务器
            userid = payload['data']['id']
            user = {}
            for k in redisdb.hkeys(userid):
                v = redisdb.hget(userid, k)
                user.update({k: v})
            if (user is None):
                result = falseReturn('', '找不到该用户信息')
            else:
                if int(user['login_time']) == payload['data']['login_time']:
                    result = trueReturn(user['userid'], '请求成功')
                else:
                    result = falseReturn('', 'Token已更改，请重新登录获取')
    else:
        result = falseReturn('', '没有提供认证token')
    return result
