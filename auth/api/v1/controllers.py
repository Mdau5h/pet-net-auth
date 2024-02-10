from bcrypt import hashpw, gensalt
from sqlalchemy.ext.asyncio import AsyncSession
from auth.api.v1.db_controllers import create_user_db
from auth.app.db import async_session
from auth.serializers.schema import UserRequest
from config import config


@async_session
async def create_user(user: UserRequest, session: AsyncSession):
    user.password = hashpw(bytes(user.password, 'UTF-8'), gensalt(rounds=config.SALT_ROUND))
    return await create_user_db(user, session=session)
