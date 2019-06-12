#!/bin/bash

# check if a build was already triggered
if [ -f ./build.lock ]; then
    exit 0
fi

# no build was triggerd, so lock it for now
touch ./build.lock
echo "Welcome to the Development Deployment!"

# we need to clean up all docker images
docker rmi $(docker images ls -q)
docker system prune -f

# now start building the docker-image
root_path = $PWD
source ./scripts/build_docker.sh

# remove the build lock
cd root_path
rm ./build.lock
