from __future__ import annotations

import factory

from .base_connector import BaseJdbcFactory


class BaseEsSinkConfig(BaseJdbcFactory):
    """Config for a Sink"""

    connector_class = "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    tasks_max = "1"
    connection_url =  "http://elasticsearch:9200"
    type_name = "_doc"
    transforms = "unwrap,key"
    transforms_unwrap_type = "io.debezium.transforms.ExtractNewRecordState"
    auto_create = "false"
    insert_mode = "upsert"
    pk_mode = "record_key"
    delete_enabled = "true"
    transforms_unwrap_drop_tombstones = "false"
    topics: str

class BaseEsSink(factory.DictFactory):
    """A Sink Connector"""

    name: str
    config = factory.SubFactory(BaseEsSinkConfig)
