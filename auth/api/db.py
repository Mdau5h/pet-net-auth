from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Load

from auth.api.models.users import User


async def get_user_from_db(login: str, session: AsyncSession) -> User:
    query = select(
        User
    ).options(
        Load(User).load_only(
            User.id,
            User.login,
            User.password
        ),
    ).where(User.login == login.lower())
    query_result = await session.execute(query)
    return query_result.scalar_one()
