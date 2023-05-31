from __future__ import annotations

import requests

from .. import exceptions
from .kafka_response import KafkaResponse


class HttpWrapper:
    def make_request(
        self,
        method: str,
        url: str,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int = 10,
    ) -> KafkaResponse:
        """Wrapper for making requests using requests package"""
        try:
            resp = requests.request(
                method, url, json=json, params=params, headers=headers, timeout=timeout
            )
            return self._response_factory(resp)

        except requests.RequestException as e:
            raise exceptions.KafkaRequestError(str(e))

    def _response_factory(
        self, response: requests.Response | None = None
    ) -> KafkaResponse:
        """Create a ConnectResposne from the requests response"""
        try:
            content = response.json()
        except ValueError:
            content = response.content

        return KafkaResponse(
            content=content,
            error=not response.ok,
            status_code=response.status_code,
        )
