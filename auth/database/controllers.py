from bcrypt import hashpw, gensalt
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database.db_controllers import create_user_db, get_user_by_login_db
from auth.database.utils import async_session
from auth.models.schema import UserRequest
from config import config


@async_session
async def create_user(user: UserRequest, session: AsyncSession):
    user.password = hashpw(bytes(user.password, 'UTF-8'), gensalt(rounds=config.SALT_ROUND))[2:]
    return await create_user_db(user, session=session)


@async_session
async def get_user_by_login(login: str, session: AsyncSession):
    return await get_user_by_login_db(login, session=session)
