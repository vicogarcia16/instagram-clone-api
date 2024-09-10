from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://localhost:3000",
    "https://instagram-clone-sigma-six.vercel.app",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003"    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")