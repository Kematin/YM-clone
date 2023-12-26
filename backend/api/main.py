# libs
import os
from contextlib import asynccontextmanager

# fastapi
import uvicorn
from database.connection import init_models
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routes
from routes.songs import songs_router
from routes.users import users_router

# logs
from services.logger import create_logger, logger

load_dotenv()


# lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    create_logger()
    yield


# app
app = FastAPI(lifespan=lifespan)
app.include_router(songs_router, prefix="/songs")
app.include_router(users_router, prefix="/users")


# CORS
origins = os.environ.get("ORIGINS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"message": "hello!"}


if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    except Exception as error:
        logger.critical(f"App was broken by {error}")
