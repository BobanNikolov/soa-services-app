from typing import Generator, List

from sqlalchemy.orm import sessionmaker, Session

from db.models.response_model.response_model import ServiceOut, ServiceIn
from db.models.service import Service
from db.session import engine
from core.config import settings
from fastapi import FastAPI, APIRouter, Depends
from db.base import Base
import uvicorn


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
create_tables()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ServiceInDB(ServiceIn):
    pass


@app.post("/services/add", response_model=ServiceOut)
def create_service(service_in: ServiceIn, db: Session = Depends(get_db)):
    db_service = ServiceInDB(**service_in.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@app.get("/services", response_model=List[ServiceOut])
def read_services(db: Session = Depends(get_db)):
    db_services = db.query(Service).all()
    return db_services


@app.get("/services/{id}", response_model=ServiceOut)
def read_service(id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).where(Service.id == id).one()
    return db_service


# todo: ask if the route is good
@app.put("/services/update/{id}", response_model=ServiceOut)
def update_service(id: int, service_in: ServiceIn, db: Session = Depends(get_db)):
    db_service = db.query(Service).where(Service.id == id).one()
    new_db_service = ServiceInDB(**service_in.dict())
    db_service.name = new_db_service.name
    db_service.date = new_db_service.date
    db_service.serviceType = new_db_service.serviceType
    db.merge(db_service)
    db.commit()


@app.delete("/services/delete")
def delete_service(id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).where(Service.id == id).one()
    db.delete(db_service)
    db.commit()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
