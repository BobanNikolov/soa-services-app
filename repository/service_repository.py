from operator import and_

from db.models.response_model.response_model import ServiceIn
from db.models.service import Service


def create_service(service_in: ServiceIn, db):
    db_service = Service(**service_in.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def read_services(db):
    return db.query(Service).all()


def read_service(id: int, db):
    return db.query(Service).where(Service.id == id).one()


def update_service(id: int, service_in: ServiceIn, db):
    db_service = db.query(Service).where(Service.id == id).one()
    new_db_service = Service(**service_in.dict())
    db_service.name = new_db_service.name
    db_service.date = new_db_service.date
    db_service.service_type = new_db_service.service_type
    db.commit()
    return db_service


def cancel_service(id: int, db):
    db_service = db.query(Service).where(Service.id == id).one()
    db.delete(db_service)
    db.commit()


def read_available_services(date_from: str, date_to: str, db):
    db_services = db.query(Service).filter(and_(Service.date >= date_from, Service.date <= date_to)).all()
    return db_services


def check_available_services(date: str, db):
    db_services = db.query(Service).filter(Service.date == date).all()
    if db_services.count() == 0:
        return True
    return False


def service_done(id: int, db):
    db_service = db.query(Service).where(Service.id == id).one()
    db_service.is_done = True
    db.commit()
    return db_service


class ServiceRepository:
    pass


service_repository = ServiceRepository()
