from typing import Any


class BaseEntity:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.set(k, v)

    def __setattr__(self, name: str, value: Any) -> None:
        self.set(name, value)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def set(self, key, value):
        self.__dict__[key] = value

    def __eq__(self, o: object) -> bool:
        return self._id == o._id

    @property
    def data(self):
        return self.__dict__
