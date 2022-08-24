import uuid
from typing import Optional
from pydantic import BaseModel, Field

"""
Resource: https://www.mongodb.com/languages/python/pymongo-tutorial
"""


class Species(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: Optional[str] = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "River Trout",
                "description": "thoughtful description here"
            }
        }


class SpeciesUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "River Trout",
                "description": "A newly updated description"
            }
        }
