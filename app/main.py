from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote
from app.models import Base
from app.core.db import engine


# Base.metadata.create_all(bind=engine) -> create database tables (not needed anymore since alembic exists)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "hello world!"}


# @app.exception_handler(status.HTTP_404_NOT_FOUND)
# def custom_404_handler(request: Request, exc: Exception):
#     templates = Jinja2Templates(directory="templates")
#     return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
#     # return RedirectResponse("/")  # arahkan ke menu utama jika akses 404
