from datetime import date
from pydantic import BaseModel, ConfigDict


# -------------------------
# Equipment Response
# -------------------------

class EquipmentResponse(BaseModel):
    id: int
    equipment_code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Location Response
# -------------------------

class LocationResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Base
# -------------------------

class AssignmentBase(BaseModel):
    equipment_id: int
    location_id: int
    trip_name: str
    assigned_to: str
    out_date: date
    expected_return: date
    remarks: str | None = None


# -------------------------
# Create
# -------------------------

class AssignmentCreate(AssignmentBase):
    pass


# -------------------------
# Update
# -------------------------

class AssignmentUpdate(AssignmentBase):
    pass


# -------------------------
# Return Equipment
# -------------------------

class AssignmentReturn(BaseModel):
    actual_return: date
    remarks: str | None = None


# -------------------------
# Response
# -------------------------

class AssignmentResponse(AssignmentBase):
    id: int

    actual_return: date | None = None
    status: str

    equipment: EquipmentResponse | None = None
    location: LocationResponse | None = None

    model_config = ConfigDict(from_attributes=True)