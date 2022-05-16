from typing import List, Generator, Optional

import uvicorn
from dependency_injector.wiring import Provide
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings
from db.base import Base
from db.models.response_model.response_model import ServiceOut, ServiceIn
from db.session import engine
from integration.integrations import UserService, PaymentService, NotificationService, StoreService
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


@app.post("/services/book", response_model=ServiceOut)
def book_service(service_in: ServiceIn, db: Session = Depends(get_db),
                 Authorization: Optional[str] = Header(None),
                 userService: UserService = Depends(Provide[settings.userService]),
                 storeService: StoreService = Depends(Provide[settings.storeService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "customer") or
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    if service_repository.check_available_services(service_in.date, db):
        product_price = storeService.check_price(service_in.name)
        db_service = service_repository.create_service(service_in, db)
        db_service.price = product_price
        return db_service
    else:
        raise HTTPException(status_code=404, detail="Couldn't find available services!")


@app.get("/services", response_model=List[ServiceOut])
def read_services(db: Session = Depends(get_db),
                  Authorization: Optional[str] = Header(None),
                  userService: UserService = Depends(Provide[settings.userService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    db_services = service_repository.read_services(db)
    return db_services


@app.get("/services/{id}", response_model=ServiceOut)
def read_service(id: int, db: Session = Depends(get_db),
                 Authorization: Optional[str] = Header(None),
                 userService: UserService = Depends(Provide[settings.userService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    db_service = service_repository.read_service(id, db)
    return db_service


@app.put("/services/update/{id}", response_model=ServiceOut)
def update_service(id: int, service_in: ServiceIn, db: Session = Depends(get_db),
                   Authorization: Optional[str] = Header(None),
                   userService: UserService = Depends(Provide[settings.userService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "customer") or
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    if service_repository.check_available_services(service_in.date, db):
        db_service = service_repository.update_service(id, service_in, db)
        return db_service
    else:
        raise HTTPException(status_code=404, detail="Couldn't find available services!")


@app.delete("/services/cancel")
def cancel_service(id: int, db: Session = Depends(get_db),
                   Authorization: Optional[str] = Header(None),
                   userService: UserService = Depends(Provide[settings.userService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "customer") or
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    service_repository.cancel_service(id, db)


@app.get("/available_services", response_model=List[ServiceOut])
def read_available_services(date_from: str, date_to: str, db: Session = Depends(get_db),
                            Authorization: Optional[str] = Header(None),
                            userService: UserService = Depends(Provide[settings.userService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "customer") or
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    db_services = service_repository.read_available_services(date_from, date_to, db)
    return db_services


@app.put("/services/done/{id}", response_model=ServiceOut)
def service_done(id: int, db: Session = Depends(get_db),
                 Authorization: Optional[str] = Header(None),
                 userService: UserService = Depends(Provide[settings.userService]),
                 paymentService: PaymentService = Depends(Provide[settings.paymentService]),
                 notificationService: NotificationService = Depends(Provide[settings.notificationService])):
    if (Authorization == None):
        raise HTTPException(status_code=401, detail="You need to authenticate first")

    if (
            not userService.user_contains_role(Authorization, "customer") or
            not userService.user_contains_role(Authorization, "employee") or
            not userService.user_contains_role(Authorization, "admin")
    ):
        raise HTTPException(status_code=401, detail="Forbidden access to this endpoint")
    db_service = service_repository.service_done(id, db)
    tx_service = "{serviceIds: ["+db_service.id+"]}"
    paymentService.make_payment(tx_service)
    notificationService.notify()
    return db_service


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)
