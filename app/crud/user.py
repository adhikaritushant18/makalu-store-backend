from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser(
    CRUDBase[
        User,
        UserCreate,
        UserCreate,
    ]
):
    pass


user = CRUDUser(User)