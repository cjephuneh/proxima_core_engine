# Core Engine Manager

Proxima Core Engine

## Prerequisites
* Docker-CE
    * https://docs.docker.com/install/linux/docker-ce/ubuntu/
* Docker Compose
    * https://docs.docker.com/compose/install/


## Installation

### Docker
#### Clone the repo
Clone the repository into an appropriate location.

##### SSH
```
git clone git@github.com:Proximaagent/proxima-core-engine.git
```
##### HTTPS
```
git clone https://github.com/Proximaagent/proxima-core-engine.git 
```


### Build all images

```
docker-compose build --no-cache
```

```
make dev-bash
pip install -r ../requirements/private-local-dev.txt
```

### Start all images

```
docker-compose up -d
```





