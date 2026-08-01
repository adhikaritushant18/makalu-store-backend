from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.equipment import Equipment
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
)


class CRUDEquipment(
    CRUDBase[
        Equipment,
        EquipmentCreate,
        EquipmentUpdate
    ]
):

    def get(self, db: Session, id: int):
        return (
            db.query(Equipment)
            .options(
                joinedload(Equipment.category),
                joinedload(Equipment.location)
            )
            .filter(Equipment.id == id)
            .first()
        )

    def get_filtered(
        self,
        db: Session,
        search: str | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ):

        query = (
            db.query(Equipment)
            .options(
                joinedload(Equipment.category),
                joinedload(Equipment.location)
            )
        )

        # Search by equipment code or name
        if search:
            query = query.filter(
                or_(
                    Equipment.equipment_code.ilike(f"%{search}%"),
                    Equipment.name.ilike(f"%{search}%"),
                )
            )

        # Filter by category
        if category_id:
            query = query.filter(
                Equipment.category_id == category_id
            )

        # Filter by status
        if status:
            query = query.filter(
                Equipment.status == status
            )

        return query.all()


equipment = CRUDEquipment(Equipment)