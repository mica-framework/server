from redis_db import connection
from config import config
from datetime import datetime
from flask import json
from . import get_native_attacks


# add a new job for the given victim
def add_job(hostname, command):
    connection.rpush('{}-{}'.format(hostname, config['redisDB']['keys']['attacks']['name']), command)


# save the start info within redis
def job_start(hostname, command, uuid):

    # save the uuid in the running-attacks list
    key = '{}-{}'.format(hostname, uuid)
    print("Saving UUID Key for attack: {}".format(key))
    connection.rpush('running-attacks', key)

    # now save the attack details
    value = {
        "uuid": uuid,
        "hostname": hostname,
        "command": command,
        "started": datetime.now().timestamp()
    }
    print("Saving now the given data: {}".format(json.dumps(value)))
    connection.set(key, json.dumps(value))


# delete this entry from redis - we do not need it anymore
def job_end(hostname, uuid):
    key = '{}-{}'.format(hostname, uuid)
    connection.delete(key)


# adds the attack to the set of attacks
def add_native_attack(data={}):

    # only process that
    if not data['name'] or not data['command']:
        return

    # need to save it in two steps
    # 1) save the attack as key <=> value where key is the name and value is the command
    connection.set(data['name'], data['command'])

    # 2.1) get list of native attacks and check if we already have this attack stored
    existing_attacks = get_native_attacks()

    # 2.2) save the attack_name into a list of attacks if we do not know that attack
    if data['name'] not in existing_attacks:
        connection.rpush('native-attacks', data['name'])