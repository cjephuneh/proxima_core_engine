from __future__ import annotations


class ConnectUrls:
    def __init__(self, root: str) -> None:
        self._root = root.strip("/")
        self.connectors: str = f"{self._root}/connectors"
        self.plugins: str = f"{self._root}/connector-plugins"

    def connector_config(self, name: str) -> str:
        """Return config url for connector name"""
        return self.connectors + f"/{name}/config"

    def validate_config(self, plugin_type: str) -> str:
        """Return the plugin validation endpoint for plugin_type"""
        return self.plugins + f"/{plugin_type}/config/validate"

    def status(self, name: str) -> str:
        """Return status endpoint for connector name"""
        return self.connectors + f"/{name}/status"

    def connector(self, name: str) -> str:
        """Return endpoint for connector name"""
        return self.connectors + f"/{name}"

    def pause(self, name: str) -> str:
        """Pause endpoint for connector name"""
        return f"{self.connector(name)}/pause"

    def resume(self, name: str) -> str:
        """Resume endpoint for connector name"""
        return f"{self.connector(name)}/resume"

    def task(self, name: str, task_id: str) -> str:
        """Return endpoint for connector name and task_id"""
        return f"{self.tasks(name)}/{task_id}/status"

    def tasks(self, name: str) -> str:
        """Return endpoint for connector name's tasks"""
        return f"{self.connector(name)}/tasks"

    def restart_task(self, name: str, task_id: str) -> str:
        """Return endpoint for resarting task id for connector name"""
        return f"{self.tasks(name)}/{task_id}/restart"
