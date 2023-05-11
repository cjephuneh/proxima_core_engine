import os

import factory
from .kafka_connect.connectors import BaseSource, BaseSourceConfig

_SOURCE_NAME = "core-engine"

DB_USER_ENV = "KAFKA_CONNECT_REPLICATOR_DB_USER"
DB_PASSWORD_ENV = "KAFKA_CONNECT_REPLICATOR_DB_PASSWORD"
DB_NAME_ENV = "DB_DATABASE"
DB_HOST_ENV = "DB_HOST"
DB_PORT_ENV = "DB_PORT"


class SourceConfig(BaseSourceConfig):
    connector_class = "io.debezium.connector.postgresql.PostgresConnector"
    database_server_name = "core_engine_db"
    database_hostname = os.getenv(DB_HOST_ENV)
    database_port = os.getenv(DB_PORT_ENV)
    database_user = os.getenv(DB_USER_ENV)
    database_password = os.getenv(DB_PASSWORD_ENV)
    database_dbname = os.getenv(DB_NAME_ENV)


class Source(BaseSource):
    """A Source Connector for data manager"""

    name: str = ""
    config = factory.SubFactory(SourceConfig)


class CoreEngineSource(Source):
    name = _SOURCE_NAME
    config__name = _SOURCE_NAME
    config__sink_tables: list[str] = [
        "core_engine_chat_app_chat",
        "core_engine_chat_app_message",
        "core_engine_community_app_comment",
        "core_engine_community_app_issue",
        "core_engine_community_app_community",
        "core_engine_community_app_event",
        "core_engine_community_app_thread",
        "core_engine_survey_app_survey",
        "core_engine_survey_app_response",
        "core_engine_tenant_management_app_address",
        "core_engine_tenant_management_app_metadata",
        "core_engine_tenant_management_app_products",
        "core_engine_tenant_management_app_tenant",
        "core_engine_tenant_users_app_admin",
        "core_engine_tenant_users_app_client",
        "core_engine_tenant_users_app_employee",

    ]
    config__table_prefix = "public."