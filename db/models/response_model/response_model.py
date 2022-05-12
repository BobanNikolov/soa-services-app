from datetime import date

from pydantic import BaseModel

from db.models.enumeration.service_type import ServiceType


class ServiceIn(BaseModel):
    name: str
    date: str
    is_done: bool
    service_type: str


class ServiceOut(BaseModel):
    name: str
    date: date
    is_done: bool
    service_type: ServiceType

    class Config():
        orm_mode = True
