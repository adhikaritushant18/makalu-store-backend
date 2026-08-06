from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.dashboard_service import dashboard_service
from app.auth.dependency import get_current_admin

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
):
    return dashboard_service.get_dashboard(db)