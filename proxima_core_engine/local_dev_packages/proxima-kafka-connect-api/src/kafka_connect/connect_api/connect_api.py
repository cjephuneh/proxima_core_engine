from __future__ import annotations

from .http_wrapper import HttpWrapper
from .kafka_response import KafkaResponse
from .urls import ConnectUrls


class KafkaConnectApi:
    """Kafka Connect API"""

    http_api = HttpWrapper()

    def __init__(self, root_url: str) -> None:
        self._urls = ConnectUrls(root_url)

    def get_installed_connectors(self) -> KafkaResponse:
        """Return list of installed connector names"""
        return self.http_api.make_request("get", self._urls.connectors)

    def install_connector(self, connector: dict) -> KafkaResponse:
        """Install a sinkgle new connector"""
        return self.http_api.make_request(
            "post", url=self._urls.connectors, json=connector
        )

    def update_connector_config(self, connector: dict) -> KafkaResponse:
        """Update a single existing connector"""
        return self.http_api.make_request(
            "put",
            url=self._urls.connector_config(connector["name"]),
            json=connector["config"],
        )

    def delete_connector(self, name: str) -> KafkaResponse:
        """Delete connector with name"""
        return self.http_api.make_request("delete", url=self._urls.connector(name))

    def validate_config(
        self, sink_config: dict, connector_type: str = "PostgresConnector"
    ) -> KafkaResponse:
        """Send config to validate endpoint"""
        return self.http_api.make_request(
            "put", url=self._urls.validate_config(connector_type), json=sink_config
        )

    def get_connector_status(self, name: str) -> KafkaResponse:
        """Return status for connector name"""
        return self.http_api.make_request("get", url=self._urls.status(name))

    def get_connector_config(self, name: str) -> KafkaResponse:
        """Return config for connector name"""
        return self.http_api.make_request("get", url=self._urls.connector_config(name))

    def pause_connector(self, name: str) -> KafkaResponse:
        """Pause connector"""
        return self.http_api.make_request("put", url=self._urls.pause(name))

    def resume_connector(self, name: str) -> KafkaResponse:
        """Resume connector"""
        return self.http_api.make_request("put", url=self._urls.resume(name))

    def get_tasks(self, name: str) -> KafkaResponse:
        """Return tasks for connector name"""
        return self.http_api.make_request("get", url=self._urls.tasks(name))

    def get_task(self, name: str, task_id: str) -> KafkaResponse:
        """Return status for connector name's task id"""
        return self.http_api.make_request("get", url=self._urls.task(name, task_id))

    def restart_task(self, name: str, task_id: str) -> KafkaResponse:
        """Restart task_id for connector name"""
        return self.http_api.make_request(
            "post", url=self._urls.restart_task(name, task_id)
        )
