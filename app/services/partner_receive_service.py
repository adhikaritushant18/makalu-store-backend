from datetime import datetime

from app.utils.email_service import send_receive_email
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.models.partner_receive import (
    ReceiveShipment,
    ReceiveShipmentItem,
)

from app.schemas.partner_receive import (
    ReceiveShipmentCreate,
)

from app.crud.partner_equipment import (
    get_partner_equipment,
    increase_stock,
)


class PartnerReceiveService:

    def generate_receive_no(self, db: Session):

        year = datetime.now().year

        count = (
            db.query(ReceiveShipment)
            .filter(
                ReceiveShipment.receive_no.like(f"GRN-{year}-%")
            )
            .count()
        )

        return f"GRN-{year}-{count+1:04d}"

    def receive_shipment(
        self,
        db: Session,
        shipment: ReceiveShipmentCreate,
    ):

        partner = (
            db.query(Partner)
            .filter(
                Partner.id == shipment.partner_id
            )
            .first()
        )

        if not partner:
            raise HTTPException(
                status_code=404,
                detail="Partner not found."
            )

        db_shipment = ReceiveShipment(
            partner_id=shipment.partner_id,
            receive_no=self.generate_receive_no(db),
            shipment_no=shipment.shipment_no,
            received_date=shipment.received_date,
            received_by=shipment.received_by,
            origin=shipment.origin,
            carrier=shipment.carrier,
            tracking_no=shipment.tracking_no,
            remarks=shipment.remarks,
        )

        db.add(db_shipment)
        db.flush()

        for item in shipment.items:

            equipment = get_partner_equipment(
                db,
                item.partner_equipment_id,
            )

            if not equipment:
                raise HTTPException(
                    status_code=404,
                    detail=f"Equipment ID {item.partner_equipment_id} not found."
                )

            db_item = ReceiveShipmentItem(
                shipment_id=db_shipment.id,
                partner_equipment_id=item.partner_equipment_id,
                quantity=item.quantity,
                condition=item.condition,
                remarks=item.remarks,
            )

            db.add(db_item)

            increase_stock(
                db,
                item.partner_equipment_id,
                item.quantity,
            )

        # db.commit()
        # db.refresh(db_shipment)

        # return db_shipment
        
        db.commit()
        db.refresh(shipment)

        partner = shipment.partner

        send_receive_email(
            partner.email,
            shipment
        )

        return shipment

    def get_all(self, db: Session):
        return (
            db.query(ReceiveShipment)
            .order_by(
                ReceiveShipment.received_date.desc()
            )
            .all()
        )

    def get(self, db: Session, shipment_id: int):

        shipment = (
            db.query(ReceiveShipment)
            .filter(
                ReceiveShipment.id == shipment_id
            )
            .first()
        )

        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        return shipment

    def delete(self, db: Session, shipment_id: int):

        shipment = (
            db.query(ReceiveShipment)
            .filter(
                ReceiveShipment.id == shipment_id
            )
            .first()
        )

        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        db.delete(shipment)
        db.commit()

        return {
            "message": "Shipment deleted successfully."
        }


partner_receive_service = PartnerReceiveService()