from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.partner_equipment import (
    PartnerEquipmentCreate,
    PartnerEquipmentUpdate,
    PartnerEquipmentResponse,
)

from app.services.partner_equipment_service import (
    partner_equipment_service,
)

router = APIRouter(
    prefix="/partner-equipment",
    tags=["Partner Equipment"],
)


@router.get(
    "/",
    response_model=list[PartnerEquipmentResponse],
)
def get_all(
    db: Session = Depends(get_db),
):
    return partner_equipment_service.get_all(db)


@router.get(
    "/{equipment_id}",
    response_model=PartnerEquipmentResponse,
)
def get_one(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return partner_equipment_service.get(
        db,
        equipment_id,
    )


@router.post(
    "/",
    response_model=PartnerEquipmentResponse,
)
def create(
    equipment: PartnerEquipmentCreate,
    db: Session = Depends(get_db),
):
    return partner_equipment_service.create(
        db,
        equipment,
    )


@router.put(
    "/{equipment_id}",
    response_model=PartnerEquipmentResponse,
)
def update(
    equipment_id: int,
    equipment: PartnerEquipmentUpdate,
    db: Session = Depends(get_db),
):
    return partner_equipment_service.update(
        db,
        equipment_id,
        equipment,
    )


@router.delete("/{equipment_id}")
def delete(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return partner_equipment_service.delete(
        db,
        equipment_id,
    )
