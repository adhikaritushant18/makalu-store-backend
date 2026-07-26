from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
)
from app.services.equipment_service import equipment_service
from app.auth.dependency import get_current_admin

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/", response_model=list[EquipmentResponse])
def get_equipment(search: str | None = None,
    category_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)):
    return equipment_service.get_all_equipment(db, search=search,
        category_id=category_id,
        status=status)


@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    data: EquipmentCreate,
    db: Session = Depends(get_db),
):
    return equipment_service.create_equipment(db, data)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    data: EquipmentUpdate,
    db: Session = Depends(get_db),
):
    return equipment_service.update_equipment(
        db,
        equipment_id,
        data,
    )


@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    equipment_service.delete_equipment(
        db,
        equipment_id,
    )


    return {"message": "Equipment deleted"}