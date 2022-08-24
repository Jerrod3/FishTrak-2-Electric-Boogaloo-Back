from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.species import Species, SpeciesUpdate

router = APIRouter()
COLL = 'species'


@router.post("/",
             response_description="Create a new species",
             status_code=status.HTTP_201_CREATED,
             response_model=Species)
def create_species(request: Request, species: Species = Body(...)):
    species = jsonable_encoder(species)
    new_species = request.app.database[COLL].insert_one(species)
    created_species = request.app.database[COLL].find_one(
        {"_id": new_species.inserted_id}
    )

    return created_species


@router.get("/", response_description="List all species", response_model=list[Species])
def list_species(request: Request):
    species = list(request.app.database[COLL].find(limit=100))
    return species


@router.get("/{id}", response_description="Get a single species by id", response_model=Species)
def find_species(id: str, request: Request):
    if (species := request.app.database[COLL].find_one({"_id": id})) is not None:
        return species
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Species with ID {id} not found")


@router.delete("/{id}", response_description="Delete a species")
def delete_species(id: str, request: Request, response: Response):
    delete_result = request.app.database[COLL].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Species with ID {id} not found")


@router.put("/{id}", response_description="Update a species", response_model=Species)
def update_species(id: str, request: Request, species: SpeciesUpdate = Body(...)):
    species = {k: v for k, v in species.dict().items() if v is not None}
    if len(species) >= 1:
        update_result = request.app.database[COLL].update_one(
            {"_id": id}, {"$set": species}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Species with ID {id} not found")

    if (
        existing_species := request.app.database[COLL].find_one({"_id": id})
    ) is not None:
        return existing_species

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Species with ID {id} not found")
