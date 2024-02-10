from fastapi import HTTPException, status


class UnauthorisedError(HTTPException):
    def __init__(self) -> None:
        self.detail = 'Invalid username or password'
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=self.status_code, detail=self.detail)
