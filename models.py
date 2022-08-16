from pydantic import BaseModel


# SCHEMAS
class Fisherman(BaseModel):
    first: str
    last: str
