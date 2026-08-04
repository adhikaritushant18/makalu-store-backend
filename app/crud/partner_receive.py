from sqlalchemy.orm import Session

from app.models.partner_receive import ReceiveShipment


def get_receive_shipments(db: Session):
    return (
        db.query(ReceiveShipment)
        .order_by(ReceiveShipment.received_date.desc())
        .all()
    )


def get_receive_shipment(
    db: Session,
    shipment_id: int,
):
    return (
        db.query(ReceiveShipment)
        .filter(ReceiveShipment.id == shipment_id)
        .first()
    )


def create_receive_shipment(
    db: Session,
    shipment: ReceiveShipment,
):
    db.add(shipment)
    db.flush()

    return shipment


def delete_receive_shipment(
    db: Session,
    shipment: ReceiveShipment,
):
    db.delete(shipment)