#!/bin/bash

# before starting docker, we need to configure the insecure registry
cp -R /tmp/.ssh /root/.ssh
chmod 700 /root/.ssh
chmod 644 /root/.ssh/id_rsa.pub
chmod 600 /root/.ssh/id_rsa

# first we need to start the docker-service
service docker start

# for info if the docker-service is running within the container
service docker status

# now we are able to run the gunicorn server
gunicorn -b 0.0.0.0:80 --workers 4 server