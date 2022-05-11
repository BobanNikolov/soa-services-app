from sqlalchemy import Column, Integer, String, Boolean, Date, Enum

from db.base_class import Base
from db.models.enumeration.service_type import ServiceType


class Service(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date)
    is_done = Column(Boolean)
    service_type = Column(Enum(ServiceType))
