# View utils
from django.http import QueryDict


def get_filter_from_params(params, param_map, required=False, convert_lists=False):
    filters = {}
    for param in param_map:
        param_value = params.get(param, None)
        if param_value is not None:
            if convert_lists and isinstance(param_value, list):
                # Values will be lists
                filters[param_map[param] + "__in"] = param_value
            else:
                filters[param_map[param]] = param_value
        else:
            if required:
                return None

    return filters