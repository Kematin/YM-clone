import uvicorn
from fastapi import FastAPI
from models.artists import *
from models.songs import *
from models.users import *

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "hello!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
