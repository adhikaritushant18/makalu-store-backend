from sqlalchemy.orm import Session, joinedload

from app.models.assignment import Assignment

from app.crud.assignment import assignment
from app.crud.equipment import equipment

from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentReturn,
)


class AssignmentService:

    # -----------------------------------
    # Get All Assignments
    # -----------------------------------

    def get_all_assignments(
        self,
        db: Session,
    ):
        return (
            db.query(Assignment)
            .options(
                joinedload(Assignment.equipment),
                joinedload(Assignment.location),
            )
            .all()
        )

    # -----------------------------------
    # Assign Equipment
    # -----------------------------------

    def assign_equipment(
        self,
        db: Session,
        data: AssignmentCreate,
    ):

        equipment_obj = equipment.get(
            db,
            data.equipment_id,
        )

        if not equipment_obj:
            raise ValueError("Equipment not found.")

        if equipment_obj.status != "AVAILABLE":
            raise ValueError(
                "Equipment is not available."
            )

        assignment_obj = assignment.create(
            db=db,
            obj_in=data,
        )

        equipment_obj.status = "OUT"

        db.commit()
        db.refresh(assignment_obj)

        return assignment_obj

    # -----------------------------------
    # Update Assignment
    # -----------------------------------

    def update_assignment(
        self,
        db: Session,
        assignment_id: int,
        data: AssignmentUpdate,
    ):

        db_obj = assignment.get(
            db,
            assignment_id,
        )

        if not db_obj:
            raise ValueError(
                "Assignment not found."
            )

        return assignment.update(
            db=db,
            db_obj=db_obj,
            obj_in=data,
        )

    # -----------------------------------
    # Return Equipment
    # -----------------------------------

    def return_equipment(
        self,
        db: Session,
        assignment_id: int,
        data: AssignmentReturn,
    ):

        db_obj = assignment.get(
            db,
            assignment_id,
        )

        if not db_obj:
            raise ValueError(
                "Assignment not found."
            )

        db_obj.actual_return = data.actual_return
        db_obj.remarks = data.remarks
        db_obj.status = "RETURNED"

        equipment_obj = equipment.get(
            db,
            db_obj.equipment_id,
        )

        if equipment_obj:
            equipment_obj.status = "AVAILABLE"

        db.commit()
        db.refresh(db_obj)

        return db_obj

    # -----------------------------------
    # Delete Assignment
    # -----------------------------------

    def delete_assignment(
        self,
        db: Session,
        assignment_id: int,
    ):

        db_obj = assignment.get(
            db,
            assignment_id,
        )

        if not db_obj:
            raise ValueError(
                "Assignment not found."
            )

        return assignment.delete(
            db=db,
            id=assignment_id,
        )


assignment_service = AssignmentService()