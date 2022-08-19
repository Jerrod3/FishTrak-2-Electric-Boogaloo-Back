import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from routes import router
from dotenv import dotenv_values

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    print("Closing connection")
    app.mongodb_client.close()


app.include_router(router, tags=["fishermen"], prefix="/fishermen")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
