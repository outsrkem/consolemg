import redis

dbNum = '8'
def redis_connent(dbNum):
    '''

    :param dbNum: redis 的连接库，不同业务使用不同的库。
    :return: redis连接池
    '''
    pool = redis.ConnectionPool(host='10.10.10.24', port=6379, decode_responses=True, db=dbNum)
    red = redis.Redis(connection_pool=pool)
    return red

