from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class PartnerAssignmentItemBase(BaseModel):
    partner_equipment_id: int
    quantity: int
    remarks: Optional[str] = None


class PartnerAssignmentItemCreate(PartnerAssignmentItemBase):
    pass


class PartnerAssignmentItemResponse(PartnerAssignmentItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PartnerAssignmentBase(BaseModel):
    partner_id: int
    trip_name: str
    expedition_leader: str
    assigned_by: str
    assigned_date: date
    expected_return_date: Optional[date] = None
    remarks: Optional[str] = None


class PartnerAssignmentCreate(PartnerAssignmentBase):
    items: List[PartnerAssignmentItemCreate]


class PartnerAssignmentUpdate(BaseModel):
    trip_name: Optional[str] = None
    expedition_leader: Optional[str] = None
    assigned_by: Optional[str] = None
    assigned_date: Optional[date] = None
    expected_return_date: Optional[date] = None
    remarks: Optional[str] = None


class PartnerAssignmentResponse(PartnerAssignmentBase):
    id: int
    assignment_no: str
    items: List[PartnerAssignmentItemResponse]

    model_config = ConfigDict(from_attributes=True)