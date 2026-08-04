from sqlalchemy.orm import Session

from app.models.partner_return import PartnerReturn


def get_partner_returns(db: Session):
    return (
        db.query(PartnerReturn)
        .order_by(PartnerReturn.returned_date.desc())
        .all()
    )


def get_partner_return(db: Session, return_id: int):
    return (
        db.query(PartnerReturn)
        .filter(PartnerReturn.id == return_id)
        .first()
    )


def create_partner_return(db: Session, partner_return: PartnerReturn):
    db.add(partner_return)
    db.flush()

    return partner_return


def delete_partner_return(db: Session, partner_return: PartnerReturn):
    db.delete(partner_return)