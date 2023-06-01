from __future__ import annotations

from functools import update_wrapper
from pathlib import Path

import click

from kafka_connect.connect_api import KafkaConnectApi

from .. import exceptions
from ..connectors import Connectors
from . import cli_api
from .params import connectors_path, root_url


def pass_connectors(f):
    """Loads connectors and passes them in as an arg"""

    @click.pass_context
    def inner(ctx, *args, **kwargs):
        path = ctx.parent.params["connectors_path"]
        try:
            connectors = cli_api.get_connectors(path)
        except exceptions.NoConnectorsFoundError as e:
            print(f"Error loading connectors path:\n\n{path}")
            print()
            print(e)
            exit(-1)
        return ctx.invoke(f, connectors, *args, **kwargs)

    return update_wrapper(inner, f)


@click.group()
@connectors_path
@root_url
@click.pass_context
@click.version_option(package_name="ibl-kafka-connect-api", prog_name="kafka_connect")
def cli(ctx: click.Context, url: str, connectors_path: Path):
    """Configure and communicate with kafka-connect"""
    ctx.obj = KafkaConnectApi(url)


@cli.command(help="List all installed connectors")
@click.pass_obj
def list_installed(api: KafkaConnectApi):
    """List all currently installed connectors"""
    cli_api.list_installed_connectors(api)


@cli.command(help="Get connector status")
@click.argument("name")
@click.pass_obj
def get_status(api, name: str):
    cli_api.get_connector_status(api, name)


@cli.command(help="Delete connector")
@click.argument("name")
@click.pass_obj
def delete_connector(api: KafkaConnectApi, name: str):
    cli_api.delete_connector(api, name)


@cli.command(help="Get connector config")
@click.argument("name")
@click.pass_obj
def get_config(api: KafkaConnectApi, name: str):
    cli_api.get_config(api, name)


@cli.command(help="Install connector")
@click.argument("name")
@pass_connectors
@click.pass_obj
def install_connector(api: KafkaConnectApi, connectors: Connectors, name: str):
    cli_api.install_connector(api, name, connectors)


@cli.command(help="Pause Connector")
@click.argument("name")
@click.pass_obj
def pause_connector(api: KafkaConnectApi, name: str):
    cli_api.pause_connector(api, name)


@cli.command(help="Resumse Connector")
@click.argument("name")
@click.pass_obj
def resume_connector(api: KafkaConnectApi, name: str):
    cli_api.resume_connector(api, name)


@cli.command(help="List all running tasks for connector")
@click.argument("name")
@click.pass_obj
def get_tasks(api: KafkaConnectApi, name: str):
    cli_api.get_tasks(api, name)


@cli.command(help="Get info about a specific task")
@click.argument("name")
@click.argument("task_id")
@click.pass_obj
def get_task(api: KafkaConnectApi, name: str, task_id: int):
    cli_api.get_task(api, name, task_id)


@cli.command(help="Lists all connectors we have configs for and can be installed")
@pass_connectors
def list_available(connectors: Connectors):
    cli_api.list_available(sorted(connectors.keys()))


@cli.command(help="Restart task")
@click.argument("name")
@click.argument("task_id")
@click.pass_obj
def restart_task(api: KafkaConnectApi, name: str, task_id: int):
    cli_api.restart_task(api, name, task_id)


@cli.command(help="Install missing connectors and update existing ones")
@pass_connectors
@click.pass_obj
def sync_connectors(api: KafkaConnectApi, connectors: Connectors):
    cli_api.sync_connectors(api, connectors)
