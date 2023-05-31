class KafkaConnectError(Exception):
    """Root library exception"""


class LoaderNotFoundError(KafkaConnectError):
    """Raised when no loder is found for the given file suffix"""


class NoConnectorsFoundError(KafkaConnectError):
    """Raised if connectors attribute not found in connectors python file"""


class KafkaRequestError(KafkaConnectError):
    """Raised when there is an error communicating with the kafka-connect api"""
