from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class PartnerEquipment(Base):
    __tablename__ = "partner_equipments"

    id = Column(Integer, primary_key=True, index=True)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )

    name = Column(String(150), nullable=False)

    category = Column(String(100))

    unit = Column(String(20), default="pcs")

    current_stock = Column(Integer, default=0)

    remarks = Column(Text)

    partner = relationship(
        "Partner",
        back_populates="equipments"
    )

    receive_items = relationship(
        "ReceiveShipmentItem",
        back_populates="equipment"
    )

    assignment_items = relationship(
        "PartnerAssignmentItem",
        back_populates="equipment"
    )

    return_items = relationship(
        "PartnerReturnItem",
        back_populates="equipment"
    )