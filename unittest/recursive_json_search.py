from test_data import *
from policy import POLICY


def json_search(key, input_object, role=None):
    if key in POLICY and role not in POLICY[key]:
        return []

    ret_val = []

    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                ret_val.append({k: v})

            ret_val.extend(json_search(key, v, role))
    elif isinstance(input_object, list):
        for val in input_object:
            ret_val.extend(json_search(key, val, role))

    return ret_val 
