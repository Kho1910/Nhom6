# Fill the Python code in this file
# Fill the Python code in this file
from test_data import *
from policy import policy


def json_search(key, input_object, role=None):
    ret_val = []

    # Kiểm tra quyền truy cập nếu role được cung cấp
    if role is not None:
        allowed_roles = policy.get(key, [])

        if role not in allowed_roles:
            return []

    if isinstance(input_object, dict):
        for k, v in input_object.items():

            # Tìm thấy key
            if k == key:
                temp = {k: v}
                ret_val.append(temp)

            if isinstance(v, dict):
                ret_val.extend(
                    json_search(key, v, role)
                )

            elif isinstance(v, list):
                for item in v:
                    if not isinstance(item, (str, int)):
                        ret_val.extend(
                            json_search(key, item, role)
                        )

    # Xử lý list
    elif isinstance(input_object, list):
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(
                    json_search(key, val, role)
                )

    return ret_val
