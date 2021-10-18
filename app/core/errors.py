class CustomException(Exception):
    def __init__(self, msg: str, code: str, status_code: int):
        self.msg = msg
        self.status_code = status_code if status_code else 500
        self.code = code if code else str(self.status_code)

class ModelLoadException(BaseException):
    ...