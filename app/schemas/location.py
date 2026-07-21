from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    name: str


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass



class LocationResponse(LocationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)