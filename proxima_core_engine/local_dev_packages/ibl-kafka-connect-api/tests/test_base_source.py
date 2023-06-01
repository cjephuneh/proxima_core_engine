from __future__ import annotations

import pytest

from kafka_connect.connectors import BaseSourceConfig


@pytest.mark.parametrize("prefix", ("", "public."))
def test_sink_tables_creates_joined_str(prefix):
    """Generates a concatted CSV of tables with prefix if present"""
    expected = f"{prefix}table1,{prefix}table2,{prefix}table3"

    result = BaseSourceConfig(
        sink_tables=["table1", "table2", "table3"], table_prefix=prefix
    )

    assert result["table.include.list"] == expected
