from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.partner_assignment import PartnerAssignment
from app.models.partner_return import (
    PartnerReturn,
    PartnerReturnItem,
)

from app.schemas.partner_return import (
    PartnerReturnCreate,
)

from app.crud.partner_equipment import (
    get_partner_equipment,
    increase_stock,
)


class PartnerReturnService:

    def generate_return_no(self, db: Session):

        year = datetime.now().year

        count = (
            db.query(PartnerReturn)
            .filter(
                PartnerReturn.return_no.like(f"RET-{year}-%")
            )
            .count()
        )

        return f"RET-{year}-{count+1:04d}"

    def create_return(
        self,
        db: Session,
        partner_return: PartnerReturnCreate,
    ):

        assignment = (
            db.query(PartnerAssignment)
            .filter(
                PartnerAssignment.id == partner_return.assignment_id
            )
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found."
            )

        db_return = PartnerReturn(
            assignment_id=partner_return.assignment_id,
            return_no=self.generate_return_no(db),
            returned_date=partner_return.returned_date,
            received_by=partner_return.received_by,
            remarks=partner_return.remarks,
        )

        db.add(db_return)
        db.flush()

        for item in partner_return.items:

            equipment = get_partner_equipment(
                db,
                item.partner_equipment_id,
            )

            if not equipment:
                raise HTTPException(
                    status_code=404,
                    detail=f"Equipment {item.partner_equipment_id} not found."
                )

            db_item = PartnerReturnItem(
                return_id=db_return.id,
                partner_equipment_id=item.partner_equipment_id,
                assigned_quantity=item.assigned_quantity,
                returned_quantity=item.returned_quantity,
                missing_quantity=item.missing_quantity,
                damaged_quantity=item.damaged_quantity,
                remarks=item.remarks,
            )

            db.add(db_item)

            increase_stock(
                db,
                item.partner_equipment_id,
                item.returned_quantity,
            )

        db.commit()

        db.refresh(db_return)

        return db_return

    def get_all(self, db: Session):
        return (
            db.query(PartnerReturn)
            .order_by(
                PartnerReturn.returned_date.desc()
            )
            .all()
        )

    def get(self, db: Session, return_id: int):

        partner_return = (
            db.query(PartnerReturn)
            .filter(
                PartnerReturn.id == return_id
            )
            .first()
        )

        if not partner_return:
            raise HTTPException(
                status_code=404,
                detail="Return not found."
            )

        return partner_return

    def delete(self, db: Session, return_id: int):

        partner_return = (
            db.query(PartnerReturn)
            .filter(
                PartnerReturn.id == return_id
            )
            .first()
        )

        if not partner_return:
            raise HTTPException(
                status_code=404,
                detail="Return not found."
            )

        db.delete(partner_return)
        db.commit()

        return {"message": "Return deleted successfully."}


partner_return_service = PartnerReturnService()