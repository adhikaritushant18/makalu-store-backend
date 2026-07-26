from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
)
from app.services.location_service import location_service
from app.auth.dependency import get_current_admin

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/", response_model=list[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    return location_service.get_all_locations(db)


@router.post("/", response_model=LocationResponse)
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
):
    return location_service.create_location(db, data)


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    data: LocationUpdate,
    db: Session = Depends(get_db),
):
    return location_service.update_location(
        db,
        location_id,
        data,
    )


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    location_service.delete_location(
        db,
        location_id,
    )

    return {"message": "Location deleted"}