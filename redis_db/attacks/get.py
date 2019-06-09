from redis_db import connection
from config import config
from flask import json


def get_jobs(hostname):
    # get all the jobs
    jobs = connection.lrange('{}-{}'.format(hostname, config['redisDB']['keys']['attacks']['name']), 0, -1)

    # decode the jobs if necessary
    jobs_str = []
    for job in jobs:
        try:
            job = job.decode('utf-8')
        finally:
            jobs_str.append(job)

    # return a valid "string" array
    return jobs_str


def get_job(hostname):
    job = connection.lpop('{}-{}'.format(hostname, config['redisDB']['keys']['attacks']['name']))
    if job is None or job == "":
        return ""
    else:
        return job.decode('utf-8')


def get_running_jobs():
    # get all running jobs
    running_jobs = connection.lrange('running-attacks', 0, -1)

    # now decode the jobs
    jobs = []
    for key in running_jobs:
        job_object = connection.get(key)
        jobs.append(json.loads(job_object.decode('utf-8')))

    # return those jobs
    return jobs


def get_running_job(hostname, uuid):
    # now search for the given details
    key = '{}-{}'.format(hostname, uuid)
    result = connection.get(key)
    if result:
        return json.loads(result.decode('utf-8'))
    else:
        return result


def get_native_attacks():
    # get all running jobs
    result_list = connection.lrange('native-attacks', 0, -1)

    # now decode the jobs
    data = []
    for key in result_list:
        data.append(key.decode('utf-8'))

    # return the native attack names
    return data


def get_native_attack_command(attack_name):
    command = connection.get(attack_name)
    if command:
        return command.decode('utf-8')
    else:
        return None


def is_native_attack(attack_name):
    result_list = connection.lrange('native-attacks', 0, -1)
    result_list = [item.decode('utf-8') for item in result_list if item]
    return attack_name in result_list
    