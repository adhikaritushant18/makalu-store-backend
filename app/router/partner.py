from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.partner import (
    PartnerCreate,
    PartnerUpdate,
    PartnerResponse,
)

from app.services.partner_service import (
    partner_service,
)

router = APIRouter(
    prefix="/partners",
    tags=["Partners"],
)


@router.get(
    "/",
    response_model=list[PartnerResponse],
)
def get_partners(
    db: Session = Depends(get_db),
):
    return partner_service.get_all(db)


@router.get(
    "/{partner_id}",
    response_model=PartnerResponse,
)
def get_partner(
    partner_id: int,
    db: Session = Depends(get_db),
):
    return partner_service.get(
        db,
        partner_id,
    )


@router.post(
    "/",
    response_model=PartnerResponse,
)
def create_partner(
    partner: PartnerCreate,
    db: Session = Depends(get_db),
):
    return partner_service.create(
        db,
        partner,
    )


@router.put(
    "/{partner_id}",
    response_model=PartnerResponse,
)
def update_partner(
    partner_id: int,
    partner: PartnerUpdate,
    db: Session = Depends(get_db),
):
    return partner_service.update(
        db,
        partner_id,
        partner,
    )


@router.delete("/{partner_id}")
def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db),
):
    return partner_service.delete(
        db,
        partner_id,
    )
