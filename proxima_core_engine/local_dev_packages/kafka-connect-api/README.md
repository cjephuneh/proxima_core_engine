# ibl-kafka-connect-api
A python api and CLI for interacting with the Kafka Connect REST API

## Installation
```shell
pip install git+https://github.com/ibleducation/ibl-kafka-connect-api.git
```

## Setup
The following environment variables are used:
- `KAFKA_CONNECT_ROOT_URL` - the kafka-connect url, including ports if necessary (also a CLI option)
- `KAFKA_CONNECT_CONNCTORS_PATH` - A fully qualified path to either a `.json` with connector definitions or a `.py` file with a `CONNECTORS` attribute. (Also a CLI option)

The connectors `json` or `CONNECTORS` attribute in `.py` file must be defined as:
```
{
	"connector-name-one": {...connector-config...},
	"connector-name-two": {...connector-config...},
	...
}
```

Where the `connector-config` is a dict that can be generated from the base classes defined below.

# Usage
## Subclass Sink Config
`kafka_connect.connectors.base_connectors` defines two base sink components with defaults:

- `BaseSinkConfig` - The configuration for a given sink
- `BaseSink` - A named sink with a configuration and subfactory

These are `factory.DictFactory`'s since the connect API is done via REST w/ `json` payloads.

Here's a template you can use for your sink definitions:

```python
import factory
import os

from kafka_connect.connectors import BaseSink, BaseSinkConfig

DB_USER_ENV = "KAFKA_CONNECT_REPLICATOR_DB_USER"
DB_PASSWORD_ENV = "KAFKA_CONNECT_REPLICATOR_DB_PASSWORD"
DB_NAME_ENV = "DB_DATABASE"
DB_HOST_ENV = "DB_HOST"
DB_PORT_ENV = "DB_PORT"


# subclass the BaseSinkConfig
class YourBaseSinkConfig(BaseSinkConfig):

    # set your sensible defaults for your base sink connector config
    class Params:
        db_user: str = os.getenv(DB_USER_ENV)
        db_password: str = os.getenv(DB_PASSWORD_ENV)
        db_name: str = os.getenv(DB_NAME_ENV)
        db_host: str = os.getenv(DB_HOST_ENV)
        db_port: str = os.getenv(DB_PORT_ENV)

    # see BaseSinkConfig for other defaults you may want to override


class YourBaseSink(BaseSink):
    name: str
    config: YourBaseSinkConfig = factory.SubFactory(YourBaseSinkConfig)


# Now create your individual Sink subclasses
class UserSink(YourBaseSink):
    # Unique name for the connector within kafka connect
    # Suggest the format: `ibl-<sink-app>-<source-app>-<table/model>-sink`
    name: str = "ibl-axd-dm-user-sink"

    # Topics that the connector will subscribe to - for postgres this typically looks like
    # <your-source-connector's database.server.name>.public.<source_table_name>
    config__topics: str = "ibl-dm.public.core_user"

    # Table name in your sink database to insert this data into
    config__table_name_format: str = "edx_core_student"

    # The column from the incoming data that you will use as the primary key
    config__pk_fields: str = "id"


# Another example
class PlatformSink(YourBaseSink):
    name: str = "ibl-axd-dm-platform-sink"
    config__topics: str = "ibl-dm.public.core_platform"
    config__table_name_format: str = "edx_core_platform"
    config__pk_fields: str = "id"
```
There are also `BaseSource` and `BaseSourceConfig` to use for sources with a similar format.

## Creating `connectors.py`
Use the following template for creating your connectors:

```python
# connectors.py
import your_sinks

_CONNECTORS = [
  your_sinks.UserSink(),
  your_sinks.PlatformSink(),
  ...
]

CONNECTORS = {x["name"]: x for x in _CONNECTORS}

```

# CLI Usgae
Use the `konnect` command to list out usage:

```shell
(venv) shell> konnect
Usage: konnect [OPTIONS] COMMAND [ARGS]...

  Configure and communicate with kafka-connect

Options:
  --connectors-path PATH  Path to connectors file. Either .py w/ CONNECTORS
                          dict defined or .json. Default from
                          KAFKA_CONNECT_CONNECTORS_PATH env var.
  --url TEXT              Kafka-Connect url. Default from
                          KAFKA_CONNECT_ROOT_URL env var.
  --version               Show the version and exit.
  --help                  Show this message and exit.

Commands:
  delete-connector   Delete connector
  get-config         Get connector config
  get-status         Get connector status
  get-task           Get info about a specific task
  get-tasks          List all running tasks for connector
  install-connector  Install connector
  list-available     Lists all connectors we have configs for and can be...
  list-installed     List all installed connectors
  pause-connector    Pause Connector
  restart-task       Restart task
  resume-connector   Resumse Connector
  sync-connectors    Install missing connectors and update existing ones
```
