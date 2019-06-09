from redis_db import connection
from config import config
from datetime import datetime
from redis_db import victims


VICTIM_CACHING_TIME_MINUTES = 2


def list_victims():
    # request the data from redis
    results = connection.lrange(config['redisDB']['keys']['attacks']['name'], 0, -1)

    # now normalize it to utf-8 strings
    normalized = []
    for r in results:
        # decode to utf-8 string
        victim = r.decode('utf-8')

        # check each victim, if it may is still alive
        ttl_timestamp = get_ttl(victim)
        if ttl_timestamp is "" or ttl_timestamp is None:
            ttl_timestamp = 0

        ttl_timestamp_conv = float(ttl_timestamp)
        if (datetime.now().timestamp() - ttl_timestamp_conv) > (VICTIM_CACHING_TIME_MINUTES*60):
            victims.set.remove_victim_by_hostname(victim)
        else:
            normalized.append(victim)

    # if there are any duplicates (which should not happen btw!) remove those
    normalized = list(set(normalized))

    # finally sort the victim list
    normalized.sort()

    return normalized


def get_ttl(hostname):
    return connection.get('{}_TTL'.format(hostname))
