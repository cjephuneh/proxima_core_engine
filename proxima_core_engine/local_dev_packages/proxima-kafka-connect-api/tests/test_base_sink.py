from __future__ import annotations

from kafka_connect.connectors import BaseSinkConfig


def test_jdbc_cnx_string():
    """The jdbc connection string is properly built"""

    expected = (
        "jdbc:postgresql://some.domain:5432/my_db?user=my_user"
        "&password=my_password&stringtype=unspecified"
    )

    result = BaseSinkConfig(
        db_user="my_user",
        db_password="my_password",
        db_name="my_db",
        db_host="some.domain",
        db_port=5432,
    )

    assert result["connection.url"] == expected


def test_db_extra_kwargs_are_added():
    """db_extra_kwargs are added to the end of the connection string"""

    expected = (
        "jdbc:postgresql://some.domain:5432/my_db?user=my_user"
        "&password=my_password&stringtype=unspecified&extra_arg1=1&extra_arg2=2"
    )

    result = BaseSinkConfig(
        db_user="my_user",
        db_password="my_password",
        db_name="my_db",
        db_host="some.domain",
        db_port=5432,
        db_extra_kwargs={"extra_arg1": 1, "extra_arg2": 2},
    )

    assert result["connection.url"] == expected
