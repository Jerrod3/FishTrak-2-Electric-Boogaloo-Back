import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import create_fisherman, fetch_all_fishermen
from models import Fisherman

app = FastAPI()

origins = ['http://localhost:3000']  # this list is the approved connections for this API.
# Currently it only contains the default React connection point

#  origins = ["*"]  # this commented out list allows the API to be accessed by anybody

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def my_func():
    return "Hello World"


@app.get("/")
def root_route():
    return {"msg": "Hello, world!"}


"""
Fisherman routes:
"""


@app.get("/fishermen")
async def retrieve_all_fishermen() -> list[dict]:
    response = await fetch_all_fishermen()
    return response


@app.post("/fishermen", response_model=Fisherman)
async def post_fisherman(fisherman: Fisherman) -> dict:
    response = await create_fisherman(fisherman.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong.")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
