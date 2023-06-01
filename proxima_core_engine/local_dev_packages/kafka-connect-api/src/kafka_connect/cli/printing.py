from __future__ import annotations

import json
from pprint import pprint
from typing import Any


def print_json(data: Any, indent=2, sort_keys=True) -> None:
    """Pretty prints json data"""
    try:
        if isinstance(data, list):
            data = sorted(data)
        print(json.dumps(data, indent=indent, sort_keys=sort_keys))
    except ValueError:
        pprint(data)


def print_connectors(names: list[str]) -> None:
    """Prints connectors"""
    for name in sorted(names):
        print(f"- {name}")


def print_error(status_code: int, content: dict | str) -> None:
    """Print an error with status code"""
    print("Error:")
    print_json(content)
    print()
    print(f"Status Code: {status_code}")


def print_exception(e: Exception) -> None:
    """Print an exception"""
    print(f"Exception Occurred: {e.__class__.__name__}")
    print(e)
