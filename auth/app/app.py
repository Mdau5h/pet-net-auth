from fastapi import FastAPI, APIRouter
# from auth.api.dependencies import token_route

healthcheck_route = APIRouter()


@healthcheck_route.get('/v1/health')
def health_check():
    return {'status': 'ok'}


def create_app():
    app = FastAPI(title='pet-net-auth')
    app.include_router(healthcheck_route)
    # app.include_router(token_route, tags=['auth'])
    return app
