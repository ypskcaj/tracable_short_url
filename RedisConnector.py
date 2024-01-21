
import redis

# start docker redis with command "docker run -itd --name redis-test -p 6379:6379 redis"
#

class RedisConnector():
    def __init__(self, redisHost="localhost", redisPort=6379, redisAuthentication=None):
        pool = redis.ConnectionPool(host=redisHost, port=redisPort, decode_responses=True, password=redisAuthentication)
        self.redis = redis.Redis(connection_pool=pool)

if __name__ == "__main__":
    rc = RedisConnector()
    rc.redis.set("Test","Successful!", ex=3)
    print(rc.redis.get("Test"))