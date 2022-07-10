from fastapi import FastAPI
from routers import user
from routers import item
from starlette.staticfiles import StaticFiles
app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(user.router)
app.include_router(item.router)
