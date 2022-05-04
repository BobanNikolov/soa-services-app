from typing import List, Generator

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings
from db.base import Base
from db.models.response_model.response_model import ServiceOut, ServiceIn
from db.session import engine
from repository import service_repository


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


@app.post("/services/add", response_model=ServiceOut)
def create_service(service_in: ServiceIn, db: Session = Depends(get_db)):
    db_service = service_repository.create_service(service_in, db)
    return db_service


@app.get("/services", response_model=List[ServiceOut])
def read_services(db: Session = Depends(get_db)):
    db_services = service_repository.read_services(db)
    return db_services


@app.get("/services/{id}", response_model=ServiceOut)
def read_service(id: int, db: Session = Depends(get_db)):
    db_service = service_repository.read_service(id, db)
    return db_service


@app.put("/services/update/{id}", response_model=ServiceOut)
def update_service(id: int, service_in: ServiceIn, db: Session = Depends(get_db)):
    db_service = service_repository.update_service(id, service_in, db)
    return db_service


@app.delete("/services/delete")
def delete_service(id: int, db: Session = Depends(get_db)):
    service_repository.delete_service(id, db)


@app.get("/available_services", response_model=List[ServiceOut])
def read_available_services(date_from: str, date_to: str, db: Session = Depends(get_db)):
    db_services = service_repository.read_available_services(date_from, date_to, db)
    return db_services


@app.put("/services/done/{id}", response_model=ServiceOut)
def service_done(id: int, db: Session = Depends(get_db)):
    db_service = service_repository.service_done(id, db)
    return db_service


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
