from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from auth.app.db import get_session
from auth.utils.auth_methods import authenticate_user, generate_token


token_route = APIRouter()


@token_route.post('/get_token')
async def return_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(form_data.username, form_data.password, session=session)
    user_prepared = {
        "id": user.id,
        "login": user.login
    }
    token = generate_token(user_prepared)
    return {'access_token': token, 'token_type': 'Bearer'}


# @token_route.post('/check_token')
# async def check_token( ):

