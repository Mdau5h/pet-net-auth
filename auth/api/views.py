from fastapi import APIRouter
from auth.database.controllers import create_user
from auth.models.schema import UserRequest, UserResponse

routes = APIRouter()


@routes.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
async def create_user_view(user: UserRequest):
    return await create_user(user)
