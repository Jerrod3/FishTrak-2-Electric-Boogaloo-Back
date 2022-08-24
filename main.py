import uvicorn
from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from routes.fishermen import router as fishermen_router
from routes.lures import router as lures_router
from routes.water_body import router as water_bodies_router
from routes.species import router as species_router
from dotenv import dotenv_values


config = dotenv_values(".env")
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
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    print("Closing connection")
    app.mongodb_client.close()


for route, router in routers.items():
    app.include_router(router, tags=[route], prefix=f"/{route}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
