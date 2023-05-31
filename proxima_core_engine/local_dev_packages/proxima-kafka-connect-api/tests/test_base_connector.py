from __future__ import annotations

from kafka_connect.connectors import BaseJdbcFactory


def test_underscores_replaced_with_dots():
    """Keys with underscores are replaced with dots"""
    expected = {"one": "1", "one.one": "1.1", "one.two.one": "1.2.1"}

    result = BaseJdbcFactory(one="1", one_one="1.1", one_two_one="1.2.1")

    assert result == expected
