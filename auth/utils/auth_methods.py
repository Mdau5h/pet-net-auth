import datetime
import typing as t
from bcrypt import checkpw
from jwt import encode, decode
from auth.app.db import AsyncLocalSession
from auth.api.v1.db_controllers import get_user_by_login_db
from config import config


async def authenticate_user(username: str, password: str):
    async with AsyncLocalSession() as session:
        user = await get_user_by_login_db(username, session=session)
    if not user:
        return False
    if not checkpw(str.encode(password), user.password):
        return False
    return user


def generate_token(subject: t.Union[str, t.Any], scopes: t.Optional[t.List[str]] = None):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.TOKEN_EXPIRE_TIME_MINUTES)
    token_data = {
        'expire': str(expire),
        'payload': subject
    }
    if scopes:
        token_data['scopes'] = ' '.join(scopes)
    return encode(token_data, key=config.PRIVATE_KEY, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token):
    return decode(token, config.PUBLIC_KEY, algorithms=[config.JWT_ALGORITHM])
