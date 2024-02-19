from fastapi import HTTPException, status


class UnauthorisedError(HTTPException):
    def __init__(self) -> None:
        self.detail = 'Invalid username or password'
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserExistsError(HTTPException):
    def __init__(self, user_login) -> None:
        self.detail = f"User with login {user_login!r} already exists"
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)
