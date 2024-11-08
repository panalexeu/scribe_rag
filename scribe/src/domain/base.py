from abc import ABC, abstractmethod


class Serializable(ABC):

    @abstractmethod
    def serialize(self) -> str:
        """Convert the object to a JSON string."""
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, json_str: str) -> "Serializable":
        """Deserialize a JSON string to a Serializable object."""
        pass
