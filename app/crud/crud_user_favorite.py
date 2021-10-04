from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.user_favorite import UserFavorite
from app.schemas.user_favorite import UserFavoriteCreate,UserFavoriteUpdate
from typing import List
from app.conf import codes
class CRUDUserFavorite(CRUDBase[UserFavorite, UserFavoriteCreate, UserFavoriteUpdate]):
    def delete_user_report_items(self,db:Session,user_report_item_guid_list: List[str], user_id: int):
        self.update(db,filters=[UserFavorite.guid.in_(user_report_item_guid_list)],
        obj_in=UserFavoriteUpdate(
            status = codes.DELETED
        ),
        user_id=user_id
        )

user_favorite = CRUDUserFavorite(UserFavorite)