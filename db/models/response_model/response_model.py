from pydantic import BaseModel


class ServiceIn(BaseModel):
    name: str
    date: str
    serviceType: str


class ServiceOut(BaseModel):
    name: str
    date: str
    serviceType: str

    class Config():
        orm_mode = True
