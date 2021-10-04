from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.user_report import UserReport
from app.schemas.user_report import UserReportCreate,UserReportUpdate
from typing import List
from app.conf import codes
class CRUDUserReport(CRUDBase[UserReport, UserReportCreate, UserReportUpdate]):

    def delete_user_report_items(self,db:Session,user_report_item_guid_list: List[str], user_id: int):
        self.update(db,filters=[UserReport.guid.in_(user_report_item_guid_list)],
        obj_in=UserReportUpdate(
            status = codes.DELETED
        ),
        user_id=user_id
        )

user_report = CRUDUserReport(UserReport)