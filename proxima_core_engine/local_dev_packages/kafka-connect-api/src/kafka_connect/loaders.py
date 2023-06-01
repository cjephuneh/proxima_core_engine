from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

from .constants import CONNECTORS_ATTR
from .exceptions import LoaderNotFoundError, NoConnectorsFoundError


class ConnectorLoader:
    def load(self, path: Path) -> dict[str, dict[str, Any]]:
        raise NotImplementedError


class JsonLoader(ConnectorLoader):
    def load(self, path: Path) -> dict[str, dict[str, Any]]:
        """Loads connectors from a json file

        Expected json format is:

        {
            "connector_name": {<dict config>},
            ...
        }
        """
        with path.open() as fin:
            return json.load(fin)


class PyLoader(ConnectorLoader):
    """Loads connectors from a python file"""

    def load(self, path: Path) -> dict[str, dict[str, Any]]:
        # TODO: How can we inject changing CONNECTORS_ATTR?
        try:
            return self._get_module_connectors(path.stem, CONNECTORS_ATTR)
        except NoConnectorsFoundError:
            # File is not in the path, so must add it
            sys.path.insert(0, str(path.parent))
            return self._get_module_connectors(path.stem, CONNECTORS_ATTR)

    def _get_module_connectors(
        self, module_name: str, attr: str
    ) -> dict[str, dict[str, Any]]:
        """Return connectors from module or raise NoConnectorsFoundError"""
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            raise NoConnectorsFoundError(str(e)) from e

        try:
            connectors = getattr(module, attr)
        except AttributeError as e:
            raise NoConnectorsFoundError(str(e)) from e

        if not isinstance(connectors, dict):
            raise NoConnectorsFoundError(
                f"{attr} object must be a dict, got {type(connectors)}"
            )
        return connectors


_LOADERS = {
    ".py": PyLoader,
    ".json": JsonLoader,
}


def loader_factory(path: Path) -> ConnectorLoader:
    """Returns an appropriate instance of ConnectorLoader"""
    loader = _LOADERS.get(path.suffix)
    if loader is None:
        raise LoaderNotFoundError(f"No loder found for suffix: {path.suffix}")
    return loader
