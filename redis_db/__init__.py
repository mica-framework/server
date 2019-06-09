import redis
import os
from config import config


def _test_connection(connection):
    print("Testing the Redis-Connection...")
    try:
        res = connection.keys()
        if len(res) >= 0:
            print("Connection established!")
        else:
            print("Something went wrong..\n"
                  "Please check your configuration and if the database is running!")
    except redis.ConnectionError as ex:
        print("Something went wrong..\n"
              "Please check your configuration and if the database "
              "is running! Exception={}".format(ex))


# first of all get the config of the hostname
# if a environ-variable is set, use that one! --> probably used within docker-compose
redis_host = config['redisDB']['hostname']
if os.environ['REDIS_URL'] is not None:
    redis_host = os.environ['REDIS_URL']

# now get the port
redis_port = config['redisDB']['port']

# connect to the redis-db
print("Start connecting to Redis (Host={} | Port={})".format(redis_host, redis_port))
connection = redis.Redis(host=redis_host, port=redis_port)

# finally test the connection
_test_connection(connection)
