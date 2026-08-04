from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.schemas.partner import PartnerCreate, PartnerUpdate


def get_partners(db: Session):
    return db.query(Partner).order_by(Partner.name).all()


def get_partner(db: Session, partner_id: int):
    return (
        db.query(Partner)
        .filter(Partner.id == partner_id)
        .first()
    )


def create_partner(
    db: Session,
    partner: PartnerCreate,
):
    db_partner = Partner(**partner.model_dump())

    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)

    return db_partner


def update_partner(
    db: Session,
    partner_id: int,
    partner: PartnerUpdate,
):
    db_partner = get_partner(db, partner_id)

    if not db_partner:
        return None

    update_data = partner.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_partner, key, value)

    db.commit()
    db.refresh(db_partner)

    return db_partner


def delete_partner(
    db: Session,
    partner_id: int,
):
    db_partner = get_partner(db, partner_id)

    if not db_partner:
        return False

    db.delete(db_partner)
    db.commit()

    return True