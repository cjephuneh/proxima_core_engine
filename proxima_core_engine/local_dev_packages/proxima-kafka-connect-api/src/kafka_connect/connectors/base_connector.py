from __future__ import annotations

import factory


class BaseJdbcFactory(factory.DictFactory):
    """Use _ as a . since JDBC keys all seem to use . and no _'s"""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = super()._create(model_class, *args, **kwargs)
        return {k.replace("_", "."): v for k, v in obj.items()}
