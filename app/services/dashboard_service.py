from sqlalchemy.orm import Session

from app.models.equipment import Equipment


class DashboardService:

    def get_dashboard(self, db: Session):

        return {
            "total_equipment": db.query(Equipment).count(),

            "available": db.query(Equipment)
            .filter(
                Equipment.status == "AVAILABLE"
            )
            .count(),

            "assigned": db.query(Equipment)
            .filter(
                Equipment.status == "OUT"
            )
            .count(),

            "repair": db.query(Equipment)
            .filter(
                Equipment.status == "REPAIR"
            )
            .count(),
        }


dashboard_service = DashboardService()