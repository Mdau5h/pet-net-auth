from bcrypt import hashpw, gensalt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from auth.api.v1.db_controllers import create_user_db, get_user_by_login_db
from auth.app.db import db_transaction
from auth.serializers.schema import UserRequest
from auth.utils.exceptions import UserExistsError
from config import config


@db_transaction
async def create_user(request_params: UserRequest, session: AsyncSession):
    try:
        await get_user_by_login_db(request_params.login, session=session)
    except NoResultFound:
        request_params.password = hashpw(bytes(request_params.password, 'UTF-8'), gensalt(rounds=config.SALT_ROUND))
        return await create_user_db(request_params, session=session)
    raise UserExistsError(request_params.login)
