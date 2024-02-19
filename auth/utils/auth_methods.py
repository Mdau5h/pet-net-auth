import datetime
import typing as t
from bcrypt import checkpw
from jwt import encode, decode
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from auth.app.db import async_session, db_transaction
from auth.api.v1.db_controllers import get_user_by_login_db
from auth.utils.exceptions import UnauthorisedError
from config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@db_transaction
async def authenticate_user(login: str, password: str, session: AsyncSession):
    try:
        user = await get_user_by_login_db(login, session=session)
    except NoResultFound:
        raise UnauthorisedError()
    if not checkpw(str.encode(password), user.password):
        raise UnauthorisedError()
    return user


async def read_current_user(token: t.Annotated[str, Depends(oauth2_scheme)]):
    token_payload = decode_access_token(token=token)
    user_login = token_payload['payload']['login']
    async with async_session() as session:
        return await get_user_by_login_db(user_login, session=session)


def generate_token(subject: t.Union[str, t.Any]):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.TOKEN_EXPIRE_TIME_MINUTES)
    token_data = {
        'expire': str(expire),
        'payload': subject
    }
    return encode(token_data, key=config.PRIVATE_KEY, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token):
    return decode(token, config.PUBLIC_KEY, algorithms=[config.JWT_ALGORITHM])
