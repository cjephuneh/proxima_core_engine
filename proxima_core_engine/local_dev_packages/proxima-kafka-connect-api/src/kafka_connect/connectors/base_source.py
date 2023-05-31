from __future__ import annotations

import factory

from .base_connector import BaseJdbcFactory


class BaseSourceConfig(BaseJdbcFactory):
    class Params:
        sink_tables: list[str] = factory.lazy_attribute(lambda _: [])
        table_prefix: str = ""

    name = "replicator-source"
    connector_class = "io.debezium.connector.postgresql.PostgresConnector"
    plugin_name = "pgoutput"
    database_server_name = "db.example.domain"
    database_hostname = "postgres"
    database_port = "5432"
    database_user = "postgresuser"
    database_password = "postgrespw"
    database_dbname = "testdb"
    table_include_list = factory.LazyAttribute(lambda o: ",".join(o.sink_tables))

    @factory.lazy_attribute
    def table_include_list(self) -> str:
        """Build concatted str of {table_prefix}{table_name} for table in sink_tables"""
        tables = [f"{self.table_prefix}{table}" for table in self.sink_tables]
        return ",".join(tables)


class BaseSource(factory.DictFactory):
    """A Source Connector"""

    name: str
    config = factory.SubFactory(BaseSourceConfig)
