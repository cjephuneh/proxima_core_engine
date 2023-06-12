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

### Start all images

```
docker-compose up -d
```

### Install commands

```
docker-compose exec web pip install -r private-local.txt
```


### Setting environment variables
```
export KAFKA_CONNECT_ROOT_URL=http://debezium:8083
```

```
export KAFKA_CONNECT_CONNECTORS_PATH=/code/kafka-connect/connectors.py
```

```
export DB_USER_ENV=proximaadmin
```

```
export DB_PASSWORD_ENV=aTgLpUfKGhu
```

  git config --global user.email "proximaagents@gmail.com"
  git config --global user.name "Proxima"