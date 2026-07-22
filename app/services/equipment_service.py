from sqlalchemy.orm import Session, joinedload
from app.models.equipment import Equipment
from app.crud.equipment import equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class EquipmentService:

    def get_all_equipment(self, db: Session, search: str | None, category_id: int | None, status: str | None):
        return equipment.get_filtered(db, search=search,
        category_id=category_id,
        status=status)

    def get_equipment(self, db: Session, equipment_id: int):
        return equipment.get(db, equipment_id)

   

    def create_equipment(
        self,
        db: Session,
        data: EquipmentCreate,
    ):

        # Get the last equipment
        last_equipment = (
            db.query(Equipment)
            .order_by(Equipment.id.desc())
            .first()
        )

        if last_equipment:
            last_number = int(last_equipment.equipment_code.replace("EQ", ""))
            new_code = f"EQ{last_number + 1:05d}"
        else:
            new_code = "EQ00001"

        # Convert schema to dict
        equipment_data = data.model_dump()

        # Add generated equipment code
        equipment_data["equipment_code"] = new_code

        # Create Equipment object
        equipment_obj = Equipment(**equipment_data)

        db.add(equipment_obj)
        db.commit()
        db.refresh(equipment_obj)

        return equipment_obj

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

        db_obj = (
            db.query(Equipment)
            .options(joinedload(Equipment.assignments))
            .filter(Equipment.id == equipment_id)
            .first()
        )

        if not db_obj:
            raise ValueError("Equipment not found.")

        db.delete(db_obj)
        db.commit()

        return db_obj


equipment_service = EquipmentService()