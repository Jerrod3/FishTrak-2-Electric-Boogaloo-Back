from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.fisherman import Fisherman, FishermanUpdate

router = APIRouter()
COLL = 'fishermen'


@router.post("/",
             response_description="Create a new fisherman",
             status_code=status.HTTP_201_CREATED,
             response_model=Fisherman)
def create_fisherman(request: Request, fisherman: Fisherman = Body(...)):
    fisherman = jsonable_encoder(fisherman)
    new_fisherman = request.app.database[COLL].insert_one(fisherman)
    created_fisherman = request.app.database[COLL].find_one(
        {"_id": new_fisherman.inserted_id}
    )

    return created_fisherman


@router.get("/", response_description="List all fishermen", response_model=list[Fisherman])
def list_fishermen(request: Request):
    fishermen = list(request.app.database[COLL].find(limit=100))
    return fishermen


@router.get("/{id}", response_description="Get a single fisherman by id", response_model=Fisherman)
def find_fisherman(id: str, request: Request):
    if (fisherman := request.app.database[COLL].find_one({"_id": id})) is not None:
        return fisherman
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fisherman with ID {id} not found")


@router.delete("/{id}", response_description="Delete a fisherman")
def delete_fisherman(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLL].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fisherman with ID {id} not found")


@router.put("/{id}", response_description="Update a fisherman", response_model=Fisherman)
def update_fisherman(id: str, request: Request, fisherman: FishermanUpdate = Body(...)):
    fisherman = {k: v for k, v in fisherman.dict().items() if v is not None}
    if len(fisherman) >= 1:
        update_result = request.app.database[COLL].update_one(
            {"_id": id}, {"$set": fisherman}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fisherman with ID {id} not found")

    if (
        existing_fisherman := request.app.database[COLL].find_one({"_id": id})
    ) is not None:
        return existing_fisherman

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fisherman with ID {id} not found")
