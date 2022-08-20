import uuid
from typing import Optional
from pydantic import BaseModel, Field

"""
Resource: https://www.mongodb.com/languages/python/pymongo-tutorial
"""

"""
NOTE:
If specifying latitude and longitude coordinates, list the longitude first, and then latitude.

Valid longitude values are between -180 and 180, both inclusive.
Valid latitude values are between -90 and 90, both inclusive.
"""


class WaterBody(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    is_freshwater: bool = Field(...)
    is_stocked: bool = Field(...)
    location: Optional[tuple] = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Gull Lake",
                "is_freshwater": True,
                "is_stocked": False,
                "location": (73.856077, 40.848447)
            }
        }


class WaterBodyUpdate(BaseModel):
    name: Optional[str]
    is_freshwater: Optional[bool]
    is_stocked: Optional[bool]
    location: Optional[dict] = Field({"type": "Point", "coordinates": ...})

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Gull Lake",
                "is_freshwater": False,
                "is_stocked": True
            }
        }
