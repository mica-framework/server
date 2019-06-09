from redis_db import connection
from . import get
from config import config
from datetime import datetime


def register_victim_by_hostname(hostname):
    # first check if we already registered the user!
    registered_victims = get.list_victims()
    if hostname in registered_victims:
        return

    # ok we don't know the victim, so save him!
    connection.rpush(config['redisDB']['keys']['attacks']['name'], hostname)


# update the victim time to life
def update_victim_ttl(hostname):
    connection.set('{}_TTL'.format(hostname), datetime.now().timestamp())


# delete victim from active victims lists
def remove_victim_by_hostname(hostname):
    connection.delete('{}_TTL'.format(hostname))
