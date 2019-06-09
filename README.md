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



## How to run the Server ..
The server runs as a Docker Service by using Docker Compose. So you need Docker on your system. Your host OS is not important :-)

If you'd like to run the Server on Linux, then you only need to clone this repo
followed by a configuration of the docker-compose.yml and the config.yml for database connections.

After the configuration of the docker-compose.yml and config.yml start the server by using the docker-compose command:

```bash 
$ docker-compose up --build
```

The server also starts two separated services, which are mandatory for the central MiCA-Server:
* MiCA Cache: Stores the cache data at the path `~/redis/`
* MiCA Registry: Stores images at the path `~/docker/`

<b>Windows Hints:</b>
It is mandatory to convert the file-line-endings of the script files to unix,
because the used docker-container is a Linux-based OS which requires ``LF`` endings,
not the windows ``CRLF`` endings!



## Contribution
Feel free to contribute or create issues on this project! Let me know what you think! I'm happy about every feedback! :-)
Let's create a new and modular framework for cyber attack simulations to improve the researches on detecting those.
