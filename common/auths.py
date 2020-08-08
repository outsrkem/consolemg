import jwt, datetime, time
from flask import jsonify, session
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
                result = trueReturn(data, 'login successfully', '200')

                return jsonify(result)
            else:
                return jsonify(falseReturn('', 'password error', '000'))
        except Exception as e:
            return ("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))

    else:
        return jsonify(falseReturn('', '找不到用户', '000'))


def identify(request):
    """
    用户鉴权
    :return: list
    """
    auth_header = request.headers.get('X-Auth-Token')
    userid = request.cookies.get('userid')
    if auth_header != "" and auth_header != None:
        auth_tokenArr = auth_header.split(" ")
        auth_token = auth_tokenArr[0]
    else:
        if userid is not None:
            redisdb = redis_connent()  # 连接redis 服务器
            try:
                auth_tokenArr = redisdb.get("Token-" + userid).split(" ")
            except Exception as e:
                print ("异常:[%s] [%s]  [%s]" % (e.__traceback__.tb_lineno, e.__traceback__.tb_frame.f_globals['__file__'], e))
                print("701状态码，获取redis中token异常")
                result = falseReturn('', '获取redis中token异常','701')
                return jsonify(result)
            auth_token = auth_tokenArr[0]
        else:
            result = falseReturn('', 'No authentication token is provided', '700')
            return jsonify(result)

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
                result = falseReturn('', 'The user information could not be found', '700')
            else:
                if int(user['login_time']) == payload['data']['login_time']:
                    result = trueReturn(user['userid'], 'The request is successful', '200')
                else:
                    result = falseReturn('', 'Token has changed, please log back in to get it', '000')
    else:
        result = falseReturn('', 'No authentication token is provided', '700')
    return jsonify(result)



def delUserAuthToken(userid):
    '''
    删除用户的session和redis的token
    :param userid:
    :return:
    '''
    session.clear()
    redisdb = redis_connent()  # 连接redis 服务器
    redisdb.delete("Token-" + userid)

