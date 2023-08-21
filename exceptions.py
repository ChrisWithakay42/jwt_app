from typing import Union


class APIException(Exception):
    def __init__(self, status: int = 400, title: str = 'Bad Request', detail: Union[str, None] = None):
        self.status = status
        self.title = title
        self.detail = detail
