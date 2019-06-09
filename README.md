# MiCA-Server
Welcome to the MiCA-Framwork. This a framework for a microservice-based simulation
of cyber attacks. It depends on basically 4 repositories and 3 mandatory components.

The MiCA-Server is one of the three components used within the framework.
It is also the main component which works as a kind of linkage between all three
components.

The repositories are:
* MiCA - Server
* MiCA - CLI
* MiCA - Agent
* MiCA - Dependencies

## Requirements
There's basically one big requirement. You need to have Docker installed and 
you should have at least 80 GB of disk space available for the server Docker
container. That's it :-)

## How to run the Server...
### .. on Linux
If you'd like to run the Server on Linux, then you only need to clone this repo
followed by a configuration of the docker-compose.yml (the SECRETS need an 
update ;-))

As soon as you pre-configured the docker-compose.yml file you can start immediately
the server by executing the command:
```bash
$ docker-compose up --build
```

The build of the server will now be triggered followed by the startup of the
server, the mica-registry and the mica-redis database.

The mica-registry basically is a docker-registry which runs on the server, to
provide a custom docker-registry containing all images build for your purposes.

The mica-redis database works as a attack-log, which stores the triggered attacks
as well as a registry for all victims, which register at the server by running
the MiCA - Agent.


### .. on Windows
If you'd like to run the Server on Windows, then you need to clone this repo
followed by a configuration of the docker-compose.yml (the SECRETS need an 
update ;-)).

Now it is mandatory to convert the file-line-endings of the script files to unix,
because the used docker-container is a Linux-based OS which requires ``LF`` endings,
not the windows ``CRLF`` endings. Therefore run the following command inside the
project directory:

```bash
$ dos2unix ./scripts/*.sh
```

If you don't have dos2unix installed, then just install the Git-Bash. It is
integrated in that tool, and you might need it anyway.

As soon as you pre-configured the docker-compose.yml file, and formatted the 
line endings of the shell-scripts, you can start the server by executing 
the command:
```bash
$ docker-compose up --build
```

The build of the server will now be triggered followed by the startup of the
server, the mica-registry and the mica-redis database.

The mica-registry basically is a docker-registry which runs on the server, to
provide a custom docker-registry containing all images build for your purposes.

The mica-redis database works as a attack-log, which stores the triggered attacks
as well as a registry for all victims, which register at the server by running
the MiCA - Agent.
