from __future__ import annotations

import factory

from .base_connector import BaseJdbcFactory


class BaseSinkConfig(BaseJdbcFactory):
    """Config for a Sink"""

    class Params:
        """Params used to configure the db connection string"""

        db_user: str = ""
        db_password: str = ""
        db_name: str = ""
        db_host: str = ""
        db_port: str = ""
        db_jdbc_type: str = "postgresql"
        db_extra_kwargs: dict = factory.lazy_attribute(lambda _: {})

    connector_class = "io.confluent.connect.jdbc.JdbcSinkConnector"
    tasks_max = "1"
    connection_url = ""
    transforms = "unwrap"
    transforms_unwrap_type = "io.debezium.transforms.ExtractNewRecordState"
    auto_create = "false"
    insert_mode = "upsert"
    pk_mode = "record_key"
    delete_enabled = "true"
    transforms_unwrap_drop_tombstones = "false"
    topics: str
    table_name_format: str
    pk_fields: str

    @factory.lazy_attribute
    def connection_url(self):
        """Build a JDBC connection string url"""
        qps = {
            "user": self.db_user,
            "password": self.db_password,
            "stringtype": "unspecified",
        }
        qps.update(self.db_extra_kwargs)
        params = "&".join([f"{k}={v}" for k, v in qps.items()])
        return (
            f"jdbc:{self.db_jdbc_type}://{self.db_host}:{self.db_port}/{self.db_name}"
            f"?{params}"
        )


class BaseSink(factory.DictFactory):
    """A Sink Connector"""

    name: str
    config = factory.SubFactory(BaseSinkConfig)
