from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KafkaResponse:
    """Core fields for an Http Response"""

    content: dict | str | None = None
    error: bool = False
    status_code: int | None = None
