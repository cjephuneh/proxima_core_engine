from __future__ import annotations

from pathlib import Path

import click

from .. import constants


def validate_connectors_path(ctx, param, value):
    """Raise BadParameter if connectors path is not specified"""
    if not value:
        raise click.BadParameter(
            (
                "No connectors path specified. Connectors path must be specified via "
                f"{constants.CONNECTORS_PATH_ENV_NAME} or using the --connectors-path "
                "option"
            )
        )
    return value


root_url = click.option(
    "--url",
    envvar=constants.ROOT_URL_ENV_NAME,
    help=f"Kafka-Connect url. Default from {constants.ROOT_URL_ENV_NAME} env var.",
)
connectors_path = click.option(
    "--connectors-path",
    type=click.Path(exists=True, path_type=Path),
    envvar=constants.CONNECTORS_PATH_ENV_NAME,
    callback=validate_connectors_path,
    help="Path to connectors file. Either .py w/ CONNECTORS dict defined or .json. "
    f"Default from {constants.CONNECTORS_PATH_ENV_NAME} env var.",
)
