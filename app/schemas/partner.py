from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class PartnerBase(BaseModel):
    name: str
    country: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    remarks: Optional[str] = None


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    remarks: Optional[str] = None


class PartnerResponse(PartnerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)