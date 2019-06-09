FROM ubuntu:18.04
MAINTAINER Andreas Zinkl "zinklandi@gmail.com"

# fix possible problems on fetching the package servers
#RUN echo "nameserver 8.8.8.8" | tee /etc/resolv.conf > /dev/null
#RUN echo "nameserver 192.168.123.1" | tee /etc/resolv.conf > /dev/null

# general updates and installations
RUN apt-get update -y && \
 apt-get upgrade -y && \
 apt-get install -y python3 python3-pip python3-dev build-essential git curl

# setup docker inside the container
RUN apt-get purge docker docker.io && \
 apt-get install -y apt-transport-https ca-certificates software-properties-common gnupg-agent
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update -y && \
 apt-get install -y docker-ce docker-ce-cli containerd.io

# now setup the project within the container
COPY server.py /app/server.py
COPY scripts/startup.sh /app/startup.sh
COPY requirements.txt /app/requirements.txt
COPY config.yml /app/config.yml
COPY ./scripts /app/scripts
COPY ./redis_db /app/redis_db
COPY ./influx /app/influx
COPY ./config /app/config
COPY ./routes /app/routes
COPY ./certs/domain.crt /etc/docker/certs.d/IM-SEC-001:5000/ca.crt
COPY ./certs/domain.crt /usr/local/share/ca-certificates/IM-SEC-001:5000.crt
WORKDIR /app

# install all python project requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# update scripts
RUN chmod +x /app/scripts/deploy_develop.sh
RUN chmod +x /app/scripts/build_docker.sh

# startup the server
# reminder: we are at the workdir /app!
CMD ["/bin/bash", "./startup.sh"]