from sqlalchemy.orm import Session

from app.crud.category import category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def get_all_categories(self, db: Session):
        return category.get_all(db)

    def get_category(self, db: Session, category_id: int):
        return category.get(db, category_id)

    def create_category(self, db: Session, data: CategoryCreate):

        existing = db.query(category.model).filter(
            category.model.name == data.name
        ).first()

        if existing:
            raise ValueError("Category already exists.")

        return category.create(
            db=db,
            obj_in=data
        )

    def update_category(
        self,
        db: Session,
        category_id: int,
        data: CategoryUpdate,
    ):

        db_obj = category.get(db, category_id)

        if not db_obj:
            raise ValueError("Category not found.")

        return category.update(
            db=db,
            db_obj=db_obj,
            obj_in=data
        )

    def delete_category(
        self,
        db: Session,
        category_id: int,
    ):

        db_obj = category.get(db, category_id)

        if not db_obj:
            raise ValueError("Category not found.")
        
        if db_obj.equipments:
            raise ValueError(
            "Cannot delete category because it is assigned to equipment."
        )

        return category.delete(
            db=db,
            id=category_id
        )


category_service = CategoryService()