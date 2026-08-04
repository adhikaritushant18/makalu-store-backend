from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PartnerAssignment(Base):
    __tablename__ = "partner_assignments"

    id = Column(Integer, primary_key=True, index=True)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )

    assignment_no = Column(String(50), unique=True, nullable=False)

    trip_name = Column(String(150), nullable=False)

    expedition_leader = Column(String(100), nullable=False)

    assigned_by = Column(String(100), nullable=False)

    assigned_date = Column(Date, nullable=False)

    expected_return_date = Column(Date)

    remarks = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    partner = relationship("Partner")

    items = relationship(
        "PartnerAssignmentItem",
        back_populates="assignment",
        cascade="all, delete-orphan"
    )

class PartnerAssignmentItem(Base):
    __tablename__ = "partner_assignment_items"

    id = Column(Integer, primary_key=True, index=True)

    assignment_id = Column(
        Integer,
        ForeignKey("partner_assignments.id"),
        nullable=False
    )

    partner_equipment_id = Column(
        Integer,
        ForeignKey("partner_equipments.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    remarks = Column(Text)

    assignment = relationship(
        "PartnerAssignment",
        back_populates="items"
    )

    equipment = relationship(
        "PartnerEquipment",
        back_populates="assignment_items"
    )    