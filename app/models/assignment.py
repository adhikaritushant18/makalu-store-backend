from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipments.id")
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id")
    )

    trip_name: Mapped[str] = mapped_column(
        String(200)
    )

    assigned_to: Mapped[str] = mapped_column(
        String(150)
    )

    out_date: Mapped[date] = mapped_column(
        Date
    )

    expected_return: Mapped[date] = mapped_column(
        Date
    )

    actual_return: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OUT"
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    equipment = relationship(
        "Equipment",
        back_populates="assignments"
    )

    location = relationship("Location")

    def __repr__(self):
        return f"<Assignment {self.trip_name}>"