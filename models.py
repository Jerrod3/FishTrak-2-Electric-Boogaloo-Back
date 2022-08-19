import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

"""
Resource: https://www.mongodb.com/languages/python/pymongo-tutorial
"""


# Models
class Fisherman(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    first: str = Field(...)
    last: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first": "Jerrod",
                "last": "Lepper",
                "email": "jlepper@basil.dog"
            }
        }


class FishermanUpdate(BaseModel):
    first: Optional[str]
    last: Optional[str]
    email: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first": "Jerrod",
                "last": "Lepper",
                "email": "jlepper@basil.cat"
            }
        }
