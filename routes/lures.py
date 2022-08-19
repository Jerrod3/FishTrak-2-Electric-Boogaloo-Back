from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.lure import Lure, LureUpdate

router = APIRouter()
COLL = 'lures'


@router.post("/",
             response_description="Create a new lure",
             status_code=status.HTTP_201_CREATED,
             response_model=Lure)
def create_lure(request: Request, lure: Lure = Body(...)):
    lure = jsonable_encoder(lure)
    new_lure = request.app.database[COLL].insert_one(lure)
    created_lure = request.app.database[COLL].find_one(
        {"_id": new_lure.inserted_id}
    )

    return created_lure


@router.get("/", response_description="List all lures", response_model=list[Lure])
def list_lures(request: Request):
    lure = list(request.app.database[COLL].find(limit=100))
    return lure


@router.get("/{id}", response_description="Get a single lure by id", response_model=Lure)
def find_lure(id: str, request: Request):
    if (lure := request.app.database[COLL].find_one({"_id": id})) is not None:
        return lure
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lure with ID {id} not found")


@router.delete("/{id}", response_description="Delete a lure")
def delete_lure(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLL].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lure with ID {id} not found")


@router.put("/{id}", response_description="Update a lure", response_model=Lure)
def update_book(id: str, request: Request, lure: LureUpdate = Body(...)):
    lure = {k: v for k, v in lure.dict().items() if v is not None}
    if len(lure) >= 1:
        update_result = request.app.database[COLL].update_one(
            {"_id": id}, {"$set": lure}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lure with ID {id} not found")

    if (
        existing_lure := request.app.database[COLL].find_one({"_id": id})
    ) is not None:
        return existing_lure

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lure with ID {id} not found")
