from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import authentication, post, profile, user, notification, chat, image, hashtag
from configs.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(hashtag.router)
app.include_router(profile.router)
app.include_router(user.router)
app.include_router(notification.router)
app.include_router(chat.router)
app.include_router(image.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
