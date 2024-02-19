from typing import Optional
from fastapi import Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from auth.app.db import get_session
from auth.serializers.schema import TokenInfo, UserAuth
from auth.utils.auth_methods import authenticate_user, generate_token, verification_token


token_route = APIRouter()
security = HTTPBearer(auto_error=False)


@token_route.post('/login', response_model=TokenInfo)
async def login(
        form_data: UserAuth = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(form_data.login, form_data.password, session=session)
    jwt_payload = {
        "sub": user.login,
        "login": user.login,
        "email": user.email
    }
    token = generate_token(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


@token_route.post('/check_token')
async def check_token(
    authorization: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    return {
        'message': 'Access granted' if await verification_token(authorization, session) else 'Access denied'
    }

