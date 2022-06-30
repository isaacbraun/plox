# /plox/LoxRuntimeError.py
# Isaac Braun
# CPTR-405

class LoxRuntimeError(RuntimeError):
    def __init__(self, token, *args: object) -> None:
        super().__init__(*args)
        self.token = token

class BreakException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ContinueException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)