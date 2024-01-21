import hashlib
import json
import base62
import time

from RedisConnector import RedisConnector

# below instructions are environment setup for redis docker
# start docker redis with command "docker run -itd --name redis-test -p 6379:6379 redis"
# login to docker "docker exec -it redis-test /bin/bash"
# run command of redis cli "redis-cli"
# input any redis commands like get, set, hmset, etc

class URLConverter():
    def __init__(self, rc):
        self.rc = rc

    def shorten(self, url, label=None):
        # get the latest code from Redis
        self.rc.redis.hincrby("Code", "Current")
        code = int(self.rc.redis.hget("Code","Current"))
        # first 6 digits from time, and followed by the latest code
        t = int(time.time()*1000)
        shortURLCode = base62.encode((t & 63) << 26 | code)
        self.rc.redis.hset("URLMap", shortURLCode, url)
        if label is not None:
            self.rc.redis.hset("URLLabel", shortURLCode, label)
        return shortURLCode

    def getLong(self, newCode):
        longURL = self.rc.redis.hget("URLMap", newCode)
        label = self.rc.redis.hget("URLLabel", newCode)
        return (longURL, label)

if __name__ == "__main__":
    rc = RedisConnector()
    uc = URLConverter(rc)
    shortURLCode = uc.shorten("ABCDEF", "Test")
    print("Short URL Code = " + shortURLCode)
    (longURL, label) = uc.getLong(shortURLCode)
    if longURL is not None:
        print("Long  URL Code = " + longURL)
    if label is not None:
        print("Label          = " + label)





