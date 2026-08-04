from sqlalchemy.orm import Session

from app.models.partner_equipment import PartnerEquipment
from app.schemas.partner_equipment import (
    PartnerEquipmentCreate,
    PartnerEquipmentUpdate,
)


def get_partner_equipments(db: Session):
    return db.query(PartnerEquipment).all()


def get_partner_equipment(
    db: Session,
    equipment_id: int,
):
    return (
        db.query(PartnerEquipment)
        .filter(
            PartnerEquipment.id == equipment_id
        )
        .first()
    )


def create_partner_equipment(
    db: Session,
    equipment: PartnerEquipmentCreate,
):
    db_equipment = PartnerEquipment(
        **equipment.model_dump()
    )

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def update_partner_equipment(
    db: Session,
    equipment_id: int,
    equipment: PartnerEquipmentUpdate,
):

    db_equipment = get_partner_equipment(
        db,
        equipment_id,
    )

    if not db_equipment:
        return None

    update_data = equipment.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_equipment, key, value)

    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def delete_partner_equipment(
    db: Session,
    equipment_id: int,
):

    db_equipment = get_partner_equipment(
        db,
        equipment_id,
    )

    if not db_equipment:
        return False

    db.delete(db_equipment)
    db.commit()

    return True


def increase_stock(
    db: Session,
    equipment_id: int,
    quantity: int,
):

    equipment = get_partner_equipment(
        db,
        equipment_id,
    )

    equipment.current_stock += quantity

    return equipment


def decrease_stock(
    db: Session,
    equipment_id: int,
    quantity: int,
):

    equipment = get_partner_equipment(
        db,
        equipment_id,
    )

    if equipment.current_stock < quantity:
        return None

    equipment.current_stock -= quantity

    return equipment