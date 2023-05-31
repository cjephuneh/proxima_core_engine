from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .. import exceptions
from ..connect_api import KafkaConnectApi, KafkaResponse
from ..connectors import Connectors
from ..constants import ROOT_URL_ENV_NAME
from ..loaders import loader_factory
from . import printing


def get_connectors(path: Path) -> Connectors:
    # TODO: Make the loader take the attribute name
    loader = loader_factory(path)
    return loader().load(path)


def get_root_url() -> str:
    """Return root url from env if exists"""
    return os.getenv(ROOT_URL_ENV_NAME, "")


def connect_api_call(func):
    """Convenience wrapper for printing an error or response body

    If no request was made, the wrapped function can return None
    """

    def inner(*args, **kwargs) -> KafkaResponse:
        try:
            resp: KafkaResponse = func(*args, **kwargs)
            # No request was made
            if resp is None:
                return

            if resp.error:
                printing.print_error(resp.status_code, resp.content)
                return resp
            if resp.content:
                printing.print_json(resp.content)
            return resp
        except exceptions.KafkaRequestError as e:
            printing.print_exception(e)

    return inner


def sync_connectors(api: KafkaConnectApi, connectors: Connectors) -> None:
    """Installs missing connectors and updates existing ones"""
    try:
        installed_resp = api.get_installed_connectors()
    except exceptions.KafkaConnectError as e:
        printing.print_exception(e)
        return

    if installed_resp.error:
        printing.print_error(installed_resp.status_code, installed_resp.content)
        return

    installed = set(installed_resp.content)
    missing = connectors.keys() - installed
    existing = connectors.keys() - missing

    missing = [connectors[conn] for conn in missing]
    existing = [connectors[conn] for conn in existing]

    for config in missing:
        resp = api.install_connector(config)
        if not resp.error:
            print(f"Installed: {config['name']}")

    for config in existing:
        resp = api.update_connector_config(config)
        if not resp.error:
            print(f"Updated: {config['name']}")


@connect_api_call
def install_connector(
    api: KafkaConnectApi, connector_name: str, connectors: Connectors
) -> KafkaResponse | None:
    """Installs connector_name from connectors"""
    try:
        resp = api.install_connector(connectors[connector_name])
        if not resp.error:
            print(f"Installed: {connector_name}")
        return resp

    except KeyError as e:
        print(f"No connector named: {connector_name}")
        print()
        print("Available Connectors:")
        printing.print_connectors(sorted(connectors.keys()))


@connect_api_call
def delete_connector(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Delete connector_name from installed connectors"""
    resp = api.delete_connector(connector_name)
    if not resp.error:
        print(f"Deleted: {connector_name}")
    return resp


@connect_api_call
def list_installed_connectors(api: KafkaConnectApi) -> KafkaResponse:
    """Return all installed connectors"""
    return api.get_installed_connectors()


@connect_api_call
def get_config(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Return connector config"""
    return api.get_connector_config(connector_name)


@connect_api_call
def get_connector_status(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Return connector status for connector_name"""
    return api.get_connector_status(connector_name)


@connect_api_call
def get_tasks(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Return tasks for connector_name"""
    return api.get_tasks(connector_name)


@connect_api_call
def get_task(api: KafkaConnectApi, connector_name: str, task_id: int) -> KafkaResponse:
    """Return specific task for connector_name"""
    return api.get_task(connector_name, task_id)


@connect_api_call
def pause_connector(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Pause all tasks for given connector"""
    resp = api.pause_connector(connector_name)
    if not resp.error:
        print(f"Connector {connector_name} paused")
    return resp


@connect_api_call
def resume_connector(api: KafkaConnectApi, connector_name: str) -> KafkaResponse:
    """Resume all tasks for connector_name"""
    resp = api.resume_connector(connector_name)
    if not resp.error:
        print(f"Connector {connector_name} resumed")
    return resp


def list_available(connectors: Connectors) -> None:
    """Prints connectors"""
    printing.print_connectors(connectors)


@connect_api_call
def restart_task(
    api: KafkaConnectApi, connector_name: str, task_id: int
) -> KafkaResponse:
    """Restart task_id for connector_name"""
    resp = api.restart_task(connector_name, task_id)
    if not resp.error:
        print(f"Restarted task id {task_id} for connector {connector_name}")
    return resp
