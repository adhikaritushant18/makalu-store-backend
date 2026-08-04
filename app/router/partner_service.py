from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partner_receive import (
    ReceiveShipmentCreate,
    ReceiveShipmentResponse,
)
from app.services.partner_receive_service import partner_receive_service

router = APIRouter(
    prefix="/partner-receive",
    tags=["Partner Receive"],
)


@router.post(
    "/",
    response_model=ReceiveShipmentResponse,
)
def receive_shipment(
    shipment: ReceiveShipmentCreate,
    db: Session = Depends(get_db),
):
    return partner_receive_service.receive_shipment(
        db,
        shipment,
    )


@router.get(
    "/",
    response_model=list[ReceiveShipmentResponse],
)
def get_receive_shipments(
    db: Session = Depends(get_db),
):
    return partner_receive_service.get_receive_shipments(db)


@router.get(
    "/{shipment_id}",
    response_model=ReceiveShipmentResponse,
)
def get_receive_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
):
    return partner_receive_service.get_receive_shipment(
        db,
        shipment_id,
    )


@router.delete("/{shipment_id}")
def delete_receive_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
):
    return partner_receive_service.delete_receive_shipment(
        db,
        shipment_id,
    )