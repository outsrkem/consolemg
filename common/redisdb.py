import redis


def redis_connent():
    pool = redis.ConnectionPool(host='10.10.10.24', port=6379, decode_responses=True, db=8)
    red = redis.Redis(connection_pool=pool)
    return red
