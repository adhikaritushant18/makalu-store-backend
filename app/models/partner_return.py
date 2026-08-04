from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PartnerReturn(Base):
    __tablename__ = "partner_returns"

    id = Column(Integer, primary_key=True, index=True)

    assignment_id = Column(
        Integer,
        ForeignKey("partner_assignments.id"),
        nullable=False
    )

    return_no = Column(String(50), unique=True, nullable=False)

    returned_date = Column(Date, nullable=False)

    received_by = Column(String(100), nullable=False)

    remarks = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    assignment = relationship("PartnerAssignment")

    items = relationship(
        "PartnerReturnItem",
        back_populates="partner_return",
        cascade="all, delete-orphan"
    )

class PartnerReturnItem(Base):
    __tablename__ = "partner_return_items"

    id = Column(Integer, primary_key=True, index=True)

    return_id = Column(
        Integer,
        ForeignKey("partner_returns.id"),
        nullable=False
    )

    partner_equipment_id = Column(
        Integer,
        ForeignKey("partner_equipments.id"),
        nullable=False
    )

    assigned_quantity = Column(Integer, nullable=False)

    returned_quantity = Column(Integer, default=0)

    missing_quantity = Column(Integer, default=0)

    damaged_quantity = Column(Integer, default=0)

    remarks = Column(Text)

    partner_return = relationship(
        "PartnerReturn",
        back_populates="items"
    )

    equipment = relationship(
        "PartnerEquipment",
        back_populates="return_items"
    )    