from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class ReceiveShipmentItemEquipmentResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    unit: str = "pcs"

    model_config = ConfigDict(from_attributes=True)


class ReceiveShipmentItemBase(BaseModel):
    partner_equipment_id: int
    quantity: int
    condition: str = "Good"
    remarks: Optional[str] = None


class ReceiveShipmentItemCreate(ReceiveShipmentItemBase):
    pass


class ReceiveShipmentItemResponse(ReceiveShipmentItemBase):
    id: int
    equipment: Optional[ReceiveShipmentItemEquipmentResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ReceiveShipmentBase(BaseModel):
    partner_id: int
    shipment_no: Optional[str] = None
    receive_type: str = "SHIPMENT"
    received_date: date
    received_by: str
    origin: Optional[str] = None
    carrier: Optional[str] = None
    tracking_no: Optional[str] = None
    remarks: Optional[str] = None


class ReceiveShipmentCreate(ReceiveShipmentBase):
    items: List[ReceiveShipmentItemCreate]


from app.schemas.partner import PartnerResponse

class ReceiveShipmentResponse(ReceiveShipmentBase):
    id: int
    receive_no: str
    items: List[ReceiveShipmentItemResponse]
    partner: Optional[PartnerResponse] = None

    model_config = ConfigDict(from_attributes=True)
