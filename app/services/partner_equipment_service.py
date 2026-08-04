from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.partner_equipment import *

from app.schemas.partner_equipment import (
    PartnerEquipmentCreate,
    PartnerEquipmentUpdate,
)


class PartnerEquipmentService:

    def get_all(
        self,
        db: Session,
    ):
        return get_partner_equipments(db)

    def get(
        self,
        db: Session,
        equipment_id: int,
    ):

        equipment = get_partner_equipment(
            db,
            equipment_id,
        )

        if not equipment:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found.",
            )

        return equipment

    def create(
        self,
        db: Session,
        equipment: PartnerEquipmentCreate,
    ):
        return create_partner_equipment(
            db,
            equipment,
        )

    def update(
        self,
        db: Session,
        equipment_id: int,
        equipment: PartnerEquipmentUpdate,
    ):

        updated = update_partner_equipment(
            db,
            equipment_id,
            equipment,
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found.",
            )

        return updated

    def delete(
        self,
        db: Session,
        equipment_id: int,
    ):

        deleted = delete_partner_equipment(
            db,
            equipment_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found.",
            )

        return {
            "message": "Deleted successfully."
        }


partner_equipment_service = PartnerEquipmentService()