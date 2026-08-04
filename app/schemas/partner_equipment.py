from typing import Optional

from pydantic import BaseModel, ConfigDict


class PartnerEquipmentBase(BaseModel):
    partner_id: int
    name: str
    category: Optional[str] = None
    unit: str = "pcs"
    remarks: Optional[str] = None


class PartnerEquipmentCreate(PartnerEquipmentBase):
    pass


class PartnerEquipmentUpdate(BaseModel):
    partner_id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    remarks: Optional[str] = None


class PartnerEquipmentResponse(PartnerEquipmentBase):
    id: int
    current_stock: int

    model_config = ConfigDict(from_attributes=True)