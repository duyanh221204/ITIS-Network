from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.configs.database import Base, engine
from models import *
from routers import user, authentication, image, post, profile

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(profile.router)
app.include_router(user.router)
app.include_router(image.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
