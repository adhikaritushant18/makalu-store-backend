from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)
    country = Column(String(100))
    contact_person = Column(String(100))
    email = Column(String(150))
    phone = Column(String(50))
    remarks = Column(Text)

    equipments = relationship(
        "PartnerEquipment",
        back_populates="partner",
        cascade="all, delete-orphan"
    )