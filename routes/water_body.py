from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.water_body import WaterBody, WaterBodyUpdate

router = APIRouter()
COLL = 'water bodies'


@router.post("/",
             response_description="Create a new water body",
             status_code=status.HTTP_201_CREATED,
             response_model=WaterBody)
def create_body(request: Request, body: WaterBody = Body(...)):
    body = jsonable_encoder(body)

    # verify coordinates
    coords = body.get('location')
    if coords and len(coords) != 2:
        raise HTTPException(400, f"the provided Coordinates: {coords} are invalid. Should be (longitude, latitude)")

    new_body = request.app.database[COLL].insert_one(body)
    create_body = request.app.database[COLL].find_one(
        {"_id": new_body.inserted_id}
    )

    return create_body


@router.get("/", response_description="List all bodies", response_model=list[WaterBody])
def list_bodies(request: Request):
    bodies = list(request.app.database[COLL].find(limit=100))
    return bodies


@router.get("/{id}", response_description="Get a single water body by id", response_model=WaterBody)
def find_body(id: str, request: Request):
    if (body := request.app.database[COLL].find_one({"_id": id})) is not None:
        return body
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Water body with ID {id} not found")


@router.delete("/{id}", response_description="Delete a water body")
def delete_body(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLL].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Water body with ID {id} not found")


@router.put("/{id}", response_description="Update a water body", response_model=WaterBody)
def update_body(id: str, request: Request, body: WaterBodyUpdate = Body(...)):
    body = {k: v for k, v in body.dict().items() if v is not None}

    if 'location' in body:
        # verify coordinates
        coords = body.get('location')
        if coords and len(coords) != 2:
            raise HTTPException(400, f"the provided Coordinates: {coords} are invalid. Should be (longitude, latitude)")

    if len(body) >= 1:
        update_result = request.app.database[COLL].update_one(
            {"_id": id}, {"$set": body}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Water body with ID {id} not found")

    if (
        existing_body := request.app.database[COLL].find_one({"_id": id})
    ) is not None:
        return existing_body

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Water body with ID {id} not found")
