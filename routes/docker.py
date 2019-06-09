from flask import json, jsonify
from . import routes, __create_response__
from config import *
import multiprocessing
import subprocess
import requests
import os


# here we're using the docker command to get all the available images of the registry and return the list
"""@routes.route('list', methods=['GET'])
def image_list():

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
    return __create_response__(200, data=response.json())"""


# builds new docker containers
@routes.route('build', methods=['POST'])
def build_containers():
    th = multiprocessing.Process(target=(lambda: subprocess.call(['/bin/bash', '/app/scripts/deploy_develop.sh'])))
    th.start()
    return __create_response__(200, message='Starting the build of the containers..')
