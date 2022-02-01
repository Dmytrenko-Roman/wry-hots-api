from fastapi import FastAPI

from database import engine
from routers import heroes, users, authentication
import models


models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(heroes.router)
app.include_router(users.router)
app.include_router(authentication.router)
