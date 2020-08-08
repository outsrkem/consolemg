from datetime import datetime


def model_list(result):
    list = []
    dict = {}
    try:
        for row in result:
            for k, v in row.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    if isinstance(v, datetime):
                        v = v.strftime('%Y-%m-%d %H:%M:%S')
                    dict[k] = v
        list.append(dict)
        return list
    except Exception as e:
        return ("异常:[%s] [%d]  [%s]" % (e.__traceback__.tb_lineno, e.__traceback__.tb_frame.f_globals['__file__'], e))



def trueReturn(data, msg, code):
    return {
        "status": True,
        "data": data,
        "msg": msg,
        "code": code
    }


def falseReturn(data, msg, code):
    return {
        "status": False,
        "data": data,
        "msg": msg,
        "code": code
    }
