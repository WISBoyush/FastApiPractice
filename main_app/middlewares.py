from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from main_app.config import settings


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> JSONResponse | Response:
        authorization = request.headers.get('Authorization')
        if not authorization:
            raise HTTPException(401, "Server have not give Token")
        if authorization != f"Bearer {settings.ACCESS_TOKEN}":
            return JSONResponse(content={'detail': 'Wrong access token'}, status_code=400)

        return await call_next(request)
