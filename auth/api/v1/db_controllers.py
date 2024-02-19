from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Load
from auth.api.models.users import User
from auth.serializers.schema import UserRequest


async def create_user_db(
    request_user: UserRequest,
    session: AsyncSession
):
    user = User(
        full_name=request_user.full_name,
        phone=request_user.phone,
        email=request_user.email,
        login=request_user.login,
        password=request_user.password,
    )
    session.add(user)
    await session.commit()
    return {'id': user.id}


async def get_user_by_login_db(login: str, session: AsyncSession) -> User:
    query = select(
        User
    ).options(
        Load(User).load_only(
            User.id,
            User.login,
            User.password,
            User.email
        )
    ).where(
        User.login == login)
    query_result = await session.execute(query)
    return query_result.scalar_one()
