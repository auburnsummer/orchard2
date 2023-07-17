from typing import Any, Type

class SecretStr:
    """
    An item that can't be deserialized by msgspec easily.
    """
    _value: str

    def __init__(self, value: str):
        self._value = value

    def get_secret_value(self):
        return self._value

    def __repr__(self):
        return "************"

    def __str__(self):
        return "************"

def secret_str_hook(type: Type, obj: Any) -> SecretStr:
    if type is SecretStr:
        if isinstance(obj, str):
            return SecretStr(obj)

    raise NotImplementedError(f"value {obj} not serializable")