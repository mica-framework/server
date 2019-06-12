#!/bin/bash

echo "## Let's start building.. ##"
# this is the function which builds a docker container
function buildContainer {
  # get the arguments
  MODULE_NAME=$1

  # go to the module directory
  echo " --> Start Image-Build for Module "$MODULE_NAME

  # get the docker file
  echo " --> Downloading Dockerfile ..."
  curl "$DOCKERFILE_URL" --output Dockerfile

  echo " --> Downloading TCP Logger ..."
  # now get the tcp-logger for the conatiner
  curl https://raw.githubusercontent.com/mica-framework/tools/develop/tcp-logger/dist/TCPLogAnalyzer --output ./libs/tcp_logger

  # build the container
  echo " --> DOCKER: build "$MODULE_NAME
  DOCKER_NAME_LOWER=$(echo $MODULE_NAME | awk '{print tolower($0)}')
  docker build . -t "$DOCKER_NAME_LOWER" -q

  # need to add the push to docker registry
  echo " --> DOCKER: deploy to registry"
  docker commit "$DOCKER_NAME_LOWER" "$DOCKER_NAME_LOWER"
  REMOTE_TAG="$REGISTRY_URL"":5000/apt-toolchain/""$DOCKER_NAME_LOWER"
  echo " --> pushing $REMOTE_TAG to $REGISTRY_URL"
  docker tag "$DOCKER_NAME_LOWER" "$REMOTE_TAG"
  docker push ${REMOTE_TAG}
}

function buildNative {
  # get the arguments
  MODULE_NAME=$1

  # ok we have a native attack, so read the file line by line and save it in a single string
  ATTACK_STRING=""
  while read line; do

    # if it starts with hash, then it is a comment, and we can ignore that
    if [ "${line}" == "#"* ]; then
      continue
    fi

    # now split the possible comment from the command itself
    IFS='#' read -ra COMMAND <<< "${line}"
    line="${COMMAND[0]}"

    # if it is a empty string then skip that line too
    if [ -z "${line}" ]; then
      continue
    fi
	
    # make backslash to double backslash
    line=$(echo "$line" | sed -r 's/\\/\\\\/g')

    # now replace a double quote to a backslash double quote
    line=$(echo "$line" | sed -r 's/["]+/\\"/g')
	
    # now replace a double quote to a backslash double quote
    line=$(echo "$line" | sed -r "s/[']+/\\'/g")

    # now remove leading and trailing spaces
    line=$(echo "$line" | sed -e 's/^[ \t]*//')
  
    # now save this line, it should be a valid command
    if [ -z "$ATTACK_STRING" ]; then
      ATTACK_STRING="$line;"
    else
      ATTACK_STRING="$ATTACK_STRING $line;"
    fi
  done < "./attack.txt"
  
  # remove new lines
  ATTACK_STRING=$(echo "$ATTACK_STRING" | sed -r "s/[\n]+//g")

  # ok so now send the command to the backend
  curl -X POST -H "Content-Type: application/json" --data "{\"name\": \"$MODULE_NAME\", \"command\": \"$ATTACK_STRING\"}" "$REGISTRY_URL/api/v1/attack/add"
}

# first we need to checkout the APT-Module (develop) branch
git clone "$ATTACK_MODULE_REPOSITORY_SSH" -b ${MODULE_BRANCH}
cd "./APT-Modules/"

# Then we need to iterate over all directories within command & control, exfiltration and lateralmovement
CATEGORIES=( "exfiltration" "commandcontrol" "lateralmovement" ) #FIXME this should not be limited to only those repos!
for cat in "${CATEGORIES[@]}"
do
  category="${cat}"
  if [[ ! -d "$category" ]]; then
    continue
  fi

  cd $category
  echo "- INFO: Searching Modules in Category $category"

  for module in $PWD/*
  do
    # get the module name
    MODULE_NAME=$(basename $module)
    cd $MODULE_NAME

    # check if there's a file "attack.txt" -> no container!!!
    if [ -f "./attack.txt" ]; then
      # make use of native backends
      buildNative $MODULE_NAME
    else
      # if docker container
      buildContainer $MODULE_NAME
    fi

    # go back to the category folder
    cd ..
  done
  cd ..
done

# remove the APT-Module repository
#echo $PWD
echo "INFO: Cleanup the Folder ${PWD}"
cd ..
rm -rf "APT-Modules"

# finished everything!
echo "## Hey!! We finished the Docker-Image-Build!! ##"