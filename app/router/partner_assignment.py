from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.partner_assignment import (
    PartnerAssignmentCreate,
    PartnerAssignmentResponse,
)

from app.services.partner_assignment_service import (
    partner_assignment_service,
)

router = APIRouter(
    prefix="/partner-assignment",
    tags=["Partner Assignment"],
)


@router.post(
    "/",
    response_model=PartnerAssignmentResponse,
)
def assign_equipment(
    assignment: PartnerAssignmentCreate,
    db: Session = Depends(get_db),
):
    return partner_assignment_service.assign_equipment(
        db,
        assignment,
    )


@router.get(
    "/",
    response_model=list[PartnerAssignmentResponse],
)
def get_all(
    db: Session = Depends(get_db),
):
    return partner_assignment_service.get_all(db)


@router.get(
    "/{assignment_id}",
    response_model=PartnerAssignmentResponse,
)
def get_one(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    return partner_assignment_service.get(
        db,
        assignment_id,
    )


@router.delete("/{assignment_id}")
def delete(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    return partner_assignment_service.delete(
        db,
        assignment_id,
    )
