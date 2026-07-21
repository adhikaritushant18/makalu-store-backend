from app.crud.base import CRUDBase
from app.models.assignment import Assignment
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
)


class CRUDAssignment(
    CRUDBase[
        Assignment,
        AssignmentCreate,
        AssignmentUpdate,
    ]
):
    pass


assignment = CRUDAssignment(Assignment)