from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


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
    equipment_code: str

    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)