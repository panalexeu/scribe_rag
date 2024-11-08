import json


class Serializable[T]:

    def serialize(self, attrs: list[str]) -> str:
        """Converts the specified object attributes to a JSON string."""
        dict_ = {key: self.__dict__[key] for key in attrs}
        return json.dumps(dict_)

    @classmethod
    def deserialize(cls: type[T], json_str: str, **kwargs) -> T:
        """Deserializes a JSON string and provided kwargs to an instance of the class."""
        dict_ = json.loads(json_str)
        extended_dict = dict_ | kwargs

        return cls(**extended_dict)
