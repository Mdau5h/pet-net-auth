from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth.api.v1.controllers import create_user
from auth.app.db import get_session
from auth.serializers.schema import UserRequest, UserResponse

routes = APIRouter()


@routes.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
async def create_user_view(
        request_params: UserRequest,
        session: AsyncSession = Depends(get_session)
):
    return await create_user(request_params=request_params, session=session)
