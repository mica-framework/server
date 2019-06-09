#!/bin/bash

echo "Welcome to the Development Deployment!"

# we need to clean up all docker images
docker rmi $(docker images ls -q)
docker system prune -f

# now start building the docker-image
source ./scripts/build_docker.sh
