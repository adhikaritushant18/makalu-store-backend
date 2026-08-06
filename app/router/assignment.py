from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentReturn,
    AssignmentResponse,
)

from app.services.assignment_service import assignment_service
from app.auth.dependency import get_current_admin

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
    dependencies=[Depends(get_current_admin)],
)


# ---------------------------------------
# Get All Assignments
# ---------------------------------------

@router.get(
    "/",
    response_model=list[AssignmentResponse],
)
def get_assignments(
    db: Session = Depends(get_db),
):
    return assignment_service.get_all_assignments(db)


# ---------------------------------------
# Create Assignment
# ---------------------------------------

@router.post(
    "/",
    response_model=AssignmentResponse,
)
def assign_equipment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
):
    return assignment_service.assign_equipment(
        db,
        data,
    )


# ---------------------------------------
# Update Assignment
# ---------------------------------------

@router.put(
    "/{assignment_id}",
    response_model=AssignmentResponse,
)
def update_assignment(
    assignment_id: int,
    data: AssignmentUpdate,
    db: Session = Depends(get_db),
):
    return assignment_service.update_assignment(
        db,
        assignment_id,
        data,
    )


# ---------------------------------------
# Return Equipment
# ---------------------------------------

@router.put(
    "/{assignment_id}/return",
    response_model=AssignmentResponse,
)
def return_equipment(
    assignment_id: int,
    data: AssignmentReturn,
    db: Session = Depends(get_db),
):
    return assignment_service.return_equipment(
        db,
        assignment_id,
        data,
    )


# ---------------------------------------
# Delete Assignment
# ---------------------------------------

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    return assignment_service.delete_assignment(
        db,
        assignment_id,
    )
