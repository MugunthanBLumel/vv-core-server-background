from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_bi_report import UserBIReport
from app.schemas.user_bi_report import UserBIReportCreate, UserBIReportUpdate


class CRUDUserBIReport(CRUDBase[UserBIReport, UserBIReportCreate, UserBIReportUpdate]):
    def insert_report_users(
        self, db: Session, report_user_list: List[UserBIReport]
    ) -> None:
        """This method is used to insert report user mappings into
            user_bi_report table

        Parameters
        ----------
        db : Session
            Session object used to insert data into database
        report_user_list : List[UserBIReport]
            List of user_bi_reports

        """
        return self.batch_insert(db, obj_in=report_user_list)

    def delete_report_users(self, db, report_user_list: List[dict]) -> None:
        """This method is used to delete report user mappings into
            user_bi_report table

        Parameters
        ----------
        db : Session
            Session object used to delete data in database
        report_user_list : List[dict]
            List of user_bi_reports

        """
        return self.batch_update(db, obj_in=report_user_list)


user_bi_report = CRUDUserBIReport(UserBIReport)
