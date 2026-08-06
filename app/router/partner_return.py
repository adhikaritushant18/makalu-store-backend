from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.partner_return import (
    PartnerReturnCreate,
    PartnerReturnResponse,
)

from app.services.partner_return_service import (
    partner_return_service,
)

router = APIRouter(
    prefix="/partner-return",
    tags=["Partner Return"],
)


@router.post(
    "/",
    response_model=PartnerReturnResponse,
)
def create_return(
    partner_return: PartnerReturnCreate,
    db: Session = Depends(get_db),
):
    return partner_return_service.create_return(
        db,
        partner_return,
    )


@router.get(
    "/",
    response_model=list[PartnerReturnResponse],
)
def get_all(
    db: Session = Depends(get_db),
):
    return partner_return_service.get_all(db)


@router.get(
    "/{return_id}",
    response_model=PartnerReturnResponse,
)
def get_one(
    return_id: int,
    db: Session = Depends(get_db),
):
    return partner_return_service.get(
        db,
        return_id,
    )


@router.delete("/{return_id}")
def delete(
    return_id: int,
    db: Session = Depends(get_db),
):
    return partner_return_service.delete(
        db,
        return_id,
    )
