from abc import ABCMeta


class File(metaclass=ABCMeta):
    def __init__(self, file_name=None, ext=None, **kwargs):
        self.__dict__ = kwargs
        self.ext = ext
        self.file_name = file_name
        if not self.ext and self.file_name:
            parts = self.file_name.split(".")
            self.ext = parts[1] if len(parts) == 2 else ""

    def get_data(self):
        data = {**self.__dict__}
        del data["bot"]
        return data
