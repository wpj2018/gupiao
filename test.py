import pymysql as mysql
import redis


re = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

print(re.get("600010_2001-11-02"))
