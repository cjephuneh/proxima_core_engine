import source_connectors as source_con

_CONNECTORS = [
    source_con.CoreEngineSource(),
]

CONNECTORS = {x["name"]: x for x in _CONNECTORS}