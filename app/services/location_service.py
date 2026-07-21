from sqlalchemy.orm import Session

from app.crud.location import location
from app.schemas.location import LocationCreate, LocationUpdate


class LocationService:

    def get_all_locations(self, db: Session):
        return location.get_all(db)

    def get_location(self, db: Session, location_id: int):
        return location.get(db, location_id)

    def create_location(self, db: Session, data: LocationCreate):

        return location.create(
            db=db,
            obj_in=data
        )

    def update_location(
        self,
        db: Session,
        location_id: int,
        data: LocationUpdate,
    ):

        db_obj = location.get(db, location_id)

        if not db_obj:
            raise ValueError("Location not found.")

        return location.update(
            db=db,
            db_obj=db_obj,
            obj_in=data
        )

    def delete_location(
        self,
        db: Session,
        location_id: int,
    ):
        db_obj = location.get(db, location_id)
        
        if not db_obj:
            raise ValueError("Location not found.")

        return location.delete(
            db=db,
            id=location_id
        )


location_service = LocationService()