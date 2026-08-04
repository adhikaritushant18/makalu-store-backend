from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ReceiveShipment(Base):
    __tablename__ = "partner_receive_shipments"

    id = Column(Integer, primary_key=True, index=True)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )

    receive_no = Column(String(50), unique=True, nullable=False)
    shipment_no = Column(String(100))

    received_date = Column(Date, nullable=False)

    received_by = Column(String(100), nullable=False)

    origin = Column(String(100))
    carrier = Column(String(100))
    tracking_no = Column(String(100))

    remarks = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    partner = relationship("Partner")

    items = relationship(
        "ReceiveShipmentItem",
        back_populates="shipment",
        cascade="all, delete-orphan"
    )

class ReceiveShipmentItem(Base):
    __tablename__ = "partner_receive_shipment_items"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(
        Integer,
        ForeignKey("partner_receive_shipments.id"),
        nullable=False
    )

    partner_equipment_id = Column(
        Integer,
        ForeignKey("partner_equipments.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    condition = Column(String(50), default="Good")

    remarks = Column(Text)

    shipment = relationship(
        "ReceiveShipment",
        back_populates="items"
    )

    equipment = relationship(
        "PartnerEquipment",
        back_populates="receive_items"
    )    