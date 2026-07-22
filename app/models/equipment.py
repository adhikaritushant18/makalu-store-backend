from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id: Mapped[int] = mapped_column(primary_key=True)

    equipment_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    
    location_id: Mapped[int] = mapped_column(
    ForeignKey("locations.id"),
    nullable=False
)

    status: Mapped[str] = mapped_column(
        String(30),
        default="AVAILABLE"
    )

    remarks: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True
    )

    category = relationship(
        "Category",
        back_populates="equipments"
    )

    assignments = relationship(
        "Assignment",
        back_populates="equipment"
    )
    
    location = relationship(
    "Location",
    back_populates="equipments"
)

    def __repr__(self):
        return f"<Equipment {self.equipment_code}>"