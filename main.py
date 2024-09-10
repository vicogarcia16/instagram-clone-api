from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
if not os.getenv('PRODUCTION'):
  from dotenv import load_dotenv
  load_dotenv() 

app = FastAPI(
    title="Instagram Clone API",
    description="This is a REST API for an Instagram Clone",
    version="0.1.1",
    docs_url="/",
    redoc_url="/redoc"
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)

origins = os.getenv("ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")