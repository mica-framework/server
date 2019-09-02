# The MiCA-Server
Welcome to the MiCA-Framwork. This is one of three main components of the framework.
This is an Open-Source project, developed within my master thesis at the Laboratory of Information Security at the OTH Regensburg.
It was created within a research project about detecting and analysing of advanced persistent threat mechansims.
The goal of the server is a central component of building, storing and distributing microservice-based cyber attack mechanisms over configured victim clients running the MiCA-Agent.



## Requirements
Running the server basically requires Docker and enough disk space for storing the custom created cyber attacks on your local system. So just check the following to points:

* [ ] Docker is installed?
* [ ] You got enough space for your images: Current Image Size ~2.5 GB (each containerized attack represents one image)
* [ ] Docker is able to access the home directory of the users host-system.



## How to run the Server
The server runs as a Docker Service by using Docker Compose. So you need Docker on your system. Your host OS is not important :-)

If you'd like to run the Server on Linux, then you only need to clone this repo
followed by a configuration of the docker-compose.yml and the config.yml for database connections.

If you configured a custom influx database (which is required for storing attack logs), then just run the following command:

```bash 
docker-compose up --build
```

If you do not have an influx database within your infrastructure, then just use the provided influx-container by executing the following command.
Please note, that you need to set the config.yml file back to default if you're using the provided influx-container. Additional changes are also
possible by customizing the docker-compose YAML files.

```bash
docker-compose -f docker-compose.yml -f ./docker/influxdb.yml up --build
```

The server also starts two separated services, which are mandatory for the central MiCA-Server:
* MiCA Cache: Stores the cache data at the path `~/redis/`
* MiCA Registry: Stores images at the path `~/docker/`

<b>Windows Hints:</b>
It is mandatory to convert the file-line-endings of the script files to unix,
because the used docker-container is a Linux-based OS which requires ``LF`` endings,
not the windows ``CRLF`` endings!



## How to create your custom modules
#### 1) Create your own repo
The best way to create your custom modules and to integrate those to the build process is by creating first of all a separate
git repository. If you'd like to use a private repository, then use a deployment ssh key which allows the server to clone the
repo to the local file system for the module build. And always try to use the ssh git clone instead of the https if you need
to authenticate for a repository.

The created repository just needs to be added to the docker-compose.yml file like this:
```python
ATTACK_MODULE_REPOSITORY_SSH=git@github.com/mica-framework/modules.git
``` 

#### 2) Structure your modules
The modules repository then should currently be structured in a specific way:

```
root_directory
    |- MODULE_NAME
        |- startup.sh # a script which will execute the necessary commands to run the module immediately
        |- MODULE.rb  # the ruby metasploit modules
        |- libs       # all the dependencies need to be saved in the libs directory
            |- exploit.py
            |- dependencies.py
            |- ...
```
This Structure provides the possibility of extending the framework module by module. This also separates the modules itself, so that the build process will be able to build a microservice for each of those modules.

#### 3) Specify the Target Branch of the Modules Repo
If you'd like to use a specific branch, then just edit the entry in the docker-compose.yml:
```python
MODULE_BRANCH=master
```

#### 4) The automatic created Docker-Container File Structure
Each Docker container is structured like you see within the code section below:
```
/opt/.msf4/modules
    |- auxiliary
        |- seclab
            |- MODULE_NAME
                |- MODULE.rb  # this is the ruby metasploit module
        |- ...
    |- exploits
    | ...
/sources
    |- MODULE_NAME
        |- exploit.py
        |- dependencies.py
        |- ...
```
The module directory within the `/opt/msf4` directory contains all modules used by the Metasploit-Framework.
These are basically just the <i>MODULE.rb</i> files. The dependencies and additional sources are stored within the `/sources/` directory. There you can find the dependencies within a corresponding sub-directory which is called after the module name.

<b>Important: Please consider this structure if you're going to use dependencies and additional sources! This could may produces errors, because your local dependency paths may not be the same which invalidates the path in the docker container!</b>



## License
This project is licensed under the terms of the MIT license. See the [LICENSE](https://raw.githubusercontent.com/mica-framework/server/master/LICENSE) file.

## Contribution
Feel free to contribute or create issues on this project! Let me know what you think! I'm happy about every feedback! :-)
Let's create a new and modular framework for cyber attack simulations to improve the researches on detecting those.
