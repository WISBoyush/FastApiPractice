import uvicorn
from fastapi import FastAPI

import authors.urls
import books.urls
# from main_app.middlewares import AuthorizationMiddleware

app = FastAPI()

app.include_router(authors.urls.router)
app.include_router(books.urls.router)
# app.add_middleware(AuthorizationMiddleware)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
