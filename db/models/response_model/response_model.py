from pydantic import BaseModel
from datetime import date


class ServiceIn(BaseModel):
    name: str
    date: str
    is_done: bool
    #serviceType: str


class ServiceOut(BaseModel):
    name: str
    date: date
    is_done: bool
    #serviceType: str

    class Config():
        orm_mode = True
