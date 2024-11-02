from typing import Any


def ResponseModel(obj: Any) -> Any:
    """Formats retrieved db model for api to return."""
    if hasattr(obj, 'datetime'):
        obj.datetime = obj.datetime.strftime("%Y-%m-%d %H:%M:%S")

    return obj
