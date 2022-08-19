import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

"""
Resource: https://www.mongodb.com/languages/python/pymongo-tutorial
"""


class Lure(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    type: Optional[str] = Field(default=None)
    color: Optional[str] = Field(default=None)
    weight: Optional[float] = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Senko",
                "type": "Drop Shot",
                "color": "purple",
                "weight": 0.25
            }
        }


class LureUpdate(BaseModel):
    name: Optional[str] = Field(...)
    type: Optional[str] = Field(...)
    color: Optional[str] = Field(...)
    weight: Optional[float] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Senko",
                "type": "Drop Shot",
                "color": "red",
                "weight": 1.75
            }
        }
