from typing import Any

from .base_connector import BaseJdbcFactory
from .base_sink import BaseSink, BaseSinkConfig
from .base_source import BaseSource, BaseSourceConfig

Connectors = dict[str, dict[str, Any]]
