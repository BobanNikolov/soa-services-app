from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.enumeration.service_type import ServiceType


class Service(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date)
    # todo: ask how to implement dto
    serviceType = ServiceType
