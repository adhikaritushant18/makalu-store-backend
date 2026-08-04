from sqlalchemy.orm import Session

from app.models.partner_assignment import (
    PartnerAssignment,
)


def get_partner_assignments(db: Session):
    return (
        db.query(PartnerAssignment)
        .order_by(
            PartnerAssignment.assigned_date.desc()
        )
        .all()
    )


def get_partner_assignment(
    db: Session,
    assignment_id: int,
):
    return (
        db.query(PartnerAssignment)
        .filter(
            PartnerAssignment.id == assignment_id
        )
        .first()
    )


def create_partner_assignment(
    db: Session,
    assignment: PartnerAssignment,
):
    db.add(assignment)
    db.flush()

    return assignment


def delete_partner_assignment(
    db: Session,
    assignment: PartnerAssignment,
):
    db.delete(assignment)