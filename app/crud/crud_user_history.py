from sqlalchemy.orm.session import Session
from app.conf import codes
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from typing import List
from app.models.user_history import UserHistory
from app.schemas.user_history import UserHistoryCreate,UserHistoryUpdate

class CRUDUserHistory(CRUDBase[UserHistory, UserHistoryCreate, UserHistoryUpdate]):
    def delete_user_report_items(self,db:Session,user_report_item_guid_list: List[str], user_id: int):
        self.update(db,filters=[UserHistory.guid.in_(user_report_item_guid_list)],
        obj_in=UserHistoryUpdate(
            status = codes.DELETED
        ),
        user_id=user_id
        )

user_history = CRUDUserHistory(UserHistory)