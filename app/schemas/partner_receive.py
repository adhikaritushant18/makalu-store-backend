from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class ReceiveShipmentItemBase(BaseModel):
    partner_equipment_id: int
    quantity: int
    condition: str = "Good"
    remarks: Optional[str] = None


class ReceiveShipmentItemCreate(ReceiveShipmentItemBase):
    pass


class ReceiveShipmentItemResponse(ReceiveShipmentItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReceiveShipmentBase(BaseModel):
    partner_id: int
    shipment_no: Optional[str] = None
    received_date: date
    received_by: str
    origin: Optional[str] = None
    carrier: Optional[str] = None
    tracking_no: Optional[str] = None
    remarks: Optional[str] = None


class ReceiveShipmentCreate(ReceiveShipmentBase):
    items: List[ReceiveShipmentItemCreate]


class ReceiveShipmentResponse(ReceiveShipmentBase):
    id: int
    receive_no: str
    items: List[ReceiveShipmentItemResponse]

    model_config = ConfigDict(from_attributes=True)