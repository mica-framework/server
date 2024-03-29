# ================================================
# Welcome to the MiCA Framework - Server
# MiCA = Microservice-based Simulation of Cyber Attacks
# --
#
# This Server basically represents the core application of the whole MiCA Framework.
# It provides an API which allows a CLI, graphical UI or other Tools to create, build
# and run attack.
# MiCA comes with a Docker-Integration which means, that it creates Docker-Container,
# which contain the attack, to allow a operating system independent Framework and simulation
# of those developed Attacks.
#
# For a more detailed overview of the Server please check out the README.md.
# --
#
# Developed By
# Andreas Zinkl
# E-Mail: zinklandi@gmail.com
# ================================================
from flask import Flask
from routes import *
from config import *
from os import urandom
import multiprocessing
import subprocess
import time
import random

application = Flask(__name__)


# general definition of how a api path looks like
url_prefix = '/api/{}/'.format(str(config['version']))
application.register_blueprint(routes, url_prefix=url_prefix)


def _run_restful_api():
    if config['port'] is not None:
        print("Application is running on port {}".format(config['port']))
        application.run(port=config['port'], threaded=True, debug=True)
    else:
        print("Application is running on default port")
        application.run(threaded=True)


def _initial_image_build():
    # get a random time to wait from 5 to 10 seconds for each worker
    random.seed(urandom(5))
    time_to_wait_for_build = random.randint(5, 10)

    # now wait to start the build
    time.sleep(time_to_wait_for_build)
    subprocess.call(['/bin/bash', '/app/scripts/deploy_develop.sh'])


def run_server():
    th = multiprocessing.Process(target=_run_restful_api)
    th.start()



# startup the server if this file is called as main file
if __name__ == '__main__':
    # startup the server
    run_server()

# at startup always run an automatic build
init_thread = multiprocessing.Process(target=_initial_image_build)
init_thread.start()
