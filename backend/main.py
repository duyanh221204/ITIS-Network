from fastapi import FastAPI

from configs.database import Base, engine

from models import *

from routers import user, authentication

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(user.router)
