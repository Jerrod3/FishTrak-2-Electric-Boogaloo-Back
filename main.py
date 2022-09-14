import uvicorn
import os
from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from routes.fishermen import router as fishermen_router
from routes.lures import router as lures_router
from routes.water_body import router as water_bodies_router
from routes.species import router as species_router
from dotenv import dotenv_values


# set environmental variables based on location of Secrets
# if os.path.exists('.env'):
#     print("reading from .env file!")
#     config = dotenv_values(".env")
#     ATLAS_URI = config["ATLAS_URI"]
#     ATLAS_DB = config["DB_NAME"]
# else:
#     print("No .env file found. Hopefully the variables exist!")
#     ATLAS_URI = os.getenv("ATLAS_URI")
#     ATLAS_DB = os.getenv("DB_NAME")

ATLAS_URI = "mongodb+srv://FishTrak:GulxviwQcpGpk7Xe@cluster0.1kofm.mongodb.net/?retryWrites=true&w=majority"
ATLAS_DB = "FishTrak"

app = FastAPI()

routers: dict[str: APIRouter] = {
    'fishermen': fishermen_router,
    'lures': lures_router,
    'bodies': water_bodies_router,
    'species': species_router
}


@app.get("/")
def root_route() -> dict:
    return {"msg": "Welcome to FishTrak on the FARM stack!",
            "available routes": [f"/{key}" for key in routers]}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[ATLAS_DB]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    print("Closing connection")
    app.mongodb_client.close()


for route, router in routers.items():
    app.include_router(router, tags=[route], prefix=f"/{route}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
