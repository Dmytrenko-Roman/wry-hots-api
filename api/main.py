from fastapi import FastAPI

from database import engine
from routers import heroes, users
import models


app = FastAPI()

app.include_router(heroes.router)
app.include_router(users.router)

models.Base.metadata.create_all(engine)

