from typing import List

from sqlalchemy.orm.session import Session

from app.conf import codes
from app.crud.base import CRUDBase
from app.models.user_report import UserReport
from app.schemas.user_report import UserReportCreate, UserReportUpdate


class CRUDUserReport(CRUDBase[UserReport, UserReportCreate, UserReportUpdate]):
    def delete_user_items(
        self, db: Session, user_item_guid_list: List[str], user_id: int
    ) -> None:
        """This method is used to delete user_report records whose guid's in user_report_item_guid_list

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        user_report_item_guid_list : List[str]
            List of user_report_item guid's
        user_id : int
            user_id of the user performing delete
        """
        self.update(
            db,
            filters=[UserReport.guid.in_(user_item_guid_list)],
            obj_in=UserReportUpdate(status=codes.DELETED),
            user_id=user_id,
        )


user_report = CRUDUserReport(UserReport)
