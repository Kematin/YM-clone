# libs
import os

# fastapi
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.songs import songs_router

# routes
from routes.users import users_router

load_dotenv()

# app
app = FastAPI()
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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
