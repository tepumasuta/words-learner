from typing import Any

def _type_check(*params: tuple[Any, type, str, str]):
    for var, var_type, var_name, var_type_name in params:
        if not isinstance(var, var_type):
            raise TypeError(f"{var_name} must be {var_type_name}. Received `{var}` of type {type(var)}")
