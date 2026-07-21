from sqlalchemy.orm import Session

from app.crud.equipment import equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class EquipmentService:

    def get_all_equipment(self, db: Session):
        return equipment.get_all(db)

    def get_equipment(self, db: Session, equipment_id: int):
        return equipment.get(db, equipment_id)

    def create_equipment(
        self,
        db: Session,
        data: EquipmentCreate,
    ):

        existing = db.query(equipment.model).filter(
            equipment.model.equipment_code == data.equipment_code
        ).first()

        if existing:
            raise ValueError("Equipment code already exists.")

        return equipment.create(
            db=db,
            obj_in=data
        )

    def update_equipment(
        self,
        db: Session,
        equipment_id: int,
        data: EquipmentUpdate,
    ):

        db_obj = equipment.get(db, equipment_id)

        if not db_obj:
            raise ValueError("Equipment not found.")

        return equipment.update(
            db=db,
            db_obj=db_obj,
            obj_in=data
        )

    def delete_equipment(
        self,
        db: Session,
        equipment_id: int,
    ):

        return equipment.delete(
            db=db,
            id=equipment_id
        )


equipment_service = EquipmentService()