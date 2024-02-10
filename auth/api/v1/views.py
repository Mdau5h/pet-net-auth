from fastapi import APIRouter
from auth.api.v1.controllers import create_user
from auth.serializers.schema import UserRequest, UserResponse

routes = APIRouter()


@routes.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
async def create_user_view(user: UserRequest):
    return await create_user(user)
