from pydantic import BaseModel, ConfigDict


class EquipmentBase(BaseModel):
    name: str
    category_id: int
    status: str = "AVAILABLE"
    remarks: str | None = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    status: str | None = None
    remarks: str | None = None


class EquipmentResponse(EquipmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)