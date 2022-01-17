class BaseException(Exception):
    pass


class HandlerNotFoundException(BaseException):
    pass


class AbortProcessException(BaseException):
    def __init__(self, message) -> None:
        self.message = message


class EntityNotFoundException(BaseException):
    pass


class BadBotRequestException(BaseException):
    pass


class FileBigException(BaseException):
    def __init__(self, message) -> None:
        self.message = message


class BackendException(Exception):
    def __init__(self, response_data, status_code, uri, *args, **kwargs) -> None:
        self.response_data = response_data
        self.status_code = status_code
        self.uri = uri
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"""
        <BackendException(status_code={self.status_code}, url={self.uri}, data={self.response_data} args={self.args} kwargs={self.kwargs})>
        """
