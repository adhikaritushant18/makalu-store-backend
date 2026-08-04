from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class PartnerReturnItemBase(BaseModel):
    partner_equipment_id: int
    assigned_quantity: int
    returned_quantity: int
    missing_quantity: int = 0
    damaged_quantity: int = 0
    remarks: Optional[str] = None


class PartnerReturnItemCreate(PartnerReturnItemBase):
    pass


class PartnerReturnItemResponse(PartnerReturnItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PartnerReturnBase(BaseModel):
    assignment_id: int
    returned_date: date
    received_by: str
    remarks: Optional[str] = None


class PartnerReturnCreate(PartnerReturnBase):
    items: List[PartnerReturnItemCreate]


class PartnerReturnResponse(PartnerReturnBase):
    id: int
    return_no: str
    items: List[PartnerReturnItemResponse]

    model_config = ConfigDict(from_attributes=True)