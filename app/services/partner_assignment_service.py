from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.models.partner_equipment import PartnerEquipment
from app.models.partner_assignment import (
    PartnerAssignment,
    PartnerAssignmentItem,
)

from app.schemas.partner_assignment import (
    PartnerAssignmentCreate,
)

from app.crud.partner_equipment import (
    get_partner_equipment,
    decrease_stock,
)


class PartnerAssignmentService:

    def generate_assignment_no(self, db: Session):

        year = datetime.now().year

        count = (
            db.query(PartnerAssignment)
            .filter(
                PartnerAssignment.assignment_no.like(f"PA-{year}-%")
            )
            .count()
        )

        return f"PA-{year}-{count + 1:04d}"

    def assign_equipment(
        self,
        db: Session,
        assignment: PartnerAssignmentCreate,
    ):

        partner = (
            db.query(Partner)
            .filter(
                Partner.id == assignment.partner_id
            )
            .first()
        )

        if not partner:
            raise HTTPException(
                status_code=404,
                detail="Partner not found."
            )

        assignment_no = self.generate_assignment_no(db)

        db_assignment = PartnerAssignment(
            partner_id=assignment.partner_id,
            assignment_no=assignment_no,
            trip_name=assignment.trip_name,
            expedition_leader=assignment.expedition_leader,
            assigned_by=assignment.assigned_by,
            assigned_date=assignment.assigned_date,
            expected_return_date=assignment.expected_return_date,
            remarks=assignment.remarks,
        )

        db.add(db_assignment)

        db.flush()

        for item in assignment.items:

            equipment = get_partner_equipment(
                db,
                item.partner_equipment_id,
            )

            if not equipment:
                db.rollback()

                raise HTTPException(
                    status_code=404,
                    detail=f"Equipment ID {item.partner_equipment_id} not found."
                )

            if equipment.current_stock < item.quantity:
                db.rollback()

                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for {equipment.name}"
                )

            assignment_item = PartnerAssignmentItem(
                assignment_id=db_assignment.id,
                partner_equipment_id=item.partner_equipment_id,
                quantity=item.quantity,
                remarks=item.remarks,
            )

            db.add(assignment_item)

            decrease_stock(
                db,
                item.partner_equipment_id,
                item.quantity,
            )

        db.commit()

        db.refresh(db_assignment)

        return db_assignment

    def get_all(
        self,
        db: Session,
    ):
        return (
            db.query(PartnerAssignment)
            .order_by(
                PartnerAssignment.assigned_date.desc()
            )
            .all()
        )

    def get(
        self,
        db: Session,
        assignment_id: int,
    ):

        assignment = (
            db.query(PartnerAssignment)
            .filter(
                PartnerAssignment.id == assignment_id
            )
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found."
            )

        return assignment

    def delete(
        self,
        db: Session,
        assignment_id: int,
    ):

        assignment = (
            db.query(PartnerAssignment)
            .filter(
                PartnerAssignment.id == assignment_id
            )
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found."
            )

        db.delete(assignment)
        db.commit()

        return {
            "message": "Assignment deleted successfully."
        }


partner_assignment_service = PartnerAssignmentService()