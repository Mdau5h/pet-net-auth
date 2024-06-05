import datetime
import typing as t
from bcrypt import checkpw
from jwt import encode, decode
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials
from auth.app.db import db_transaction
from auth.api.v1.db_controllers import get_user_by_login_db
from auth.utils.exceptions import UnauthorisedError
from config import config


@db_transaction
async def authenticate_user(login: str, password: str, session: AsyncSession):
    try:
        user = await get_user_by_login_db(login, session=session)
    except NoResultFound:
        raise UnauthorisedError("User doesn't exist")
    if not checkpw(str.encode(password), user.password):
        raise UnauthorisedError('Invalid username or password')
    return user


async def verification_token(
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession
):
    try:
        token_payload = decode_access_token(token=credentials.credentials)
    # todo: make exception more specific
    except:
        return False
    user_login = token_payload['payload']['login']
    try:
        await get_user_by_login_db(user_login, session=session)
    except NoResultFound:
        return False
    return True


def generate_token(subject: t.Union[str, t.Any]):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.TOKEN_EXPIRE_TIME_MINUTES)
    token_data = {
        'expire': str(expire),
        'payload': subject
    }
    return encode(
        token_data,
        key=config.PRIVATE_KEY,
        algorithm=config.JWT_ALGORITHM
    )


def decode_access_token(token):
    return decode(
        token,
        key=config.PUBLIC_KEY,
        algorithms=[config.JWT_ALGORITHM]
    )
