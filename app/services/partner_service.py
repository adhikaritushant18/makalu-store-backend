from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.partner import (
    get_partners,
    get_partner,
    create_partner,
    update_partner,
    delete_partner,
)

from app.schemas.partner import (
    PartnerCreate,
    PartnerUpdate,
)


class PartnerService:

    def get_all(self, db: Session):
        return get_partners(db)

    def get(self, db: Session, partner_id: int):

        partner = get_partner(db, partner_id)

        if not partner:
            raise HTTPException(
                status_code=404,
                detail="Partner not found.",
            )

        return partner

    def create(
        self,
        db: Session,
        partner: PartnerCreate,
    ):
        return create_partner(db, partner)

    def update(
        self,
        db: Session,
        partner_id: int,
        partner: PartnerUpdate,
    ):
        updated = update_partner(
            db,
            partner_id,
            partner,
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Partner not found.",
            )

        return updated

    def delete(
        self,
        db: Session,
        partner_id: int,
    ):
        deleted = delete_partner(
            db,
            partner_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Partner not found.",
            )

        return {
            "message": "Partner deleted successfully."
        }


partner_service = PartnerService()