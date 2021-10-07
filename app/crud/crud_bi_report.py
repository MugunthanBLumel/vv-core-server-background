from typing import List, cast

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import distinct
from sqlalchemy.sql.functions import func

from app.conf import codes
from app.crud.base import CRUDBase
from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
from app.schemas.bi_report import (BIReportCreate, BIReportDetails,
                                   BIReportUpdate)
from app.schemas.query import JoinModel, Model, SearchQueryModel


class CRUDBIReport(CRUDBase[BIReport, BIReportCreate, BIReportUpdate]):
    def get_reports(
        self,
        db: Session,
        *,
        agent_instance_id: int,
        agent_instance_user_id_list: List[int]
    ) -> List[BIReportDetails]:
        """This method is used to get list of bi_reports along with its user mapping

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id of the reports to be fetched
        agent_instance_user_id_list : List[int]
            agent_instance_user_id_list who's reports will be fetched

        Returns
        -------
        List[BIReportDetails]
            List of bi_reports and user_mapping details
        """
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIReport.idx,
                BIReport.guid,
                BIReport.update_hash,
                UserBIReport.agent_instance_user_id,
                UserBIReport.idx.label("user_bi_report_id"),
            ],
            join=[
                JoinModel(
                    model=Model(UserBIReport),
                    relationship=[
                        BIReport.idx == UserBIReport.bi_report_id,
                        BIReport.agent_instance_id == agent_instance_id,
                        UserBIReport.agent_instance_user_id.in_(
                            agent_instance_user_id_list
                        ),
                    ],
                )
            ],
        )
        return cast(List[BIReportDetails], self.get(report_search))

    def get_reports_by_creation_time(
        self, db: Session, *, created_at: int, agent_instance_id: int, created_by: int
    ) -> List[BIReport]:
        """This method is used to get list of bi_reports by creation time along with filters
           like agent_instance_id, created_by

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        created_at : int
            time of creation of reports
        agent_instance_id : int
            agent_instance_id of the reports
        created_by : into
            created_by of the reports to be retrived

        Returns
        -------
        List[BIReport]
            List of bi_reports
        """
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[BIReport.idx, BIReport.guid],
            filters=[
                BIReport.created_at == created_at,
                BIReport.agent_instance_id == agent_instance_id,
                BIReport.created_by == created_by,
            ],
        )
        return self.get(report_search)

    def get_reports_by_guid_list(
        self, db: Session, agent_instance_id: int, report_guid_list: List[str]
    ) -> List[BIReport]:
        """This method is used to get list of bi_reports by report_guid_list including deleted reports

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id of the reports
        report_guid_list : List[str]
            List of guid's of the reports to be retrived

        Returns
        -------
        List[BIReport]
            List of bi_reports
        """
        bi_report_list: List[BIReport] = []
        start: int = 0
        end: int = len(report_guid_list)
        limit: int = 1000

        while start < end:
            slice_range: slice = slice(start, start + min(limit, end - start))
            limited_report_guid_list: List[str] = report_guid_list[slice_range]
            bi_report_list += self.get(
                SearchQueryModel(
                    db,
                    search_column=[BIReport.idx, BIReport.guid, BIReport.status],
                    filters=[
                        BIReport.agent_instance_id == agent_instance_id,
                        BIReport.guid.in_(limited_report_guid_list),
                    ],
                    exclude_default_filter=True,
                )
            )

            start += min(limit, end - start)
        return bi_report_list

    def get_reports_count(self, db: Session, agent_instance_id: int) -> int:
        """
        This method is used to get count of reports for given agent_instance_id

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id: int
            idx of agent_instance

        Returns
        -------
        int
            bi_report_count for given agent_instance_id
        """
        return self.get_count(
            SearchQueryModel(
                db,
                search_column=[distinct(BIReport.idx)],
                filters=[BIReport.agent_instance_id == agent_instance_id],
            )
        )
    
    def get_all_reports_to_be_deleted(
        self, db: Session, agent_instance_id: int
    ) -> List[int]:
        """This method is used to get list of non deleted report id's
        which doesn't have user mappings

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id's of the report
        
        Returns
        -------
        List[int]
            list of non deleted report id's which doesn't have user mappings
        """
        bi_report_id_list : List[int]= []
        report_list: List[BIReport] = self.get(
            SearchQueryModel(
                db,
                search_column=[BIReport.idx],
                join=[
                    JoinModel(
                        model=Model(UserBIReport),
                        relationship=[
                            BIReport.agent_instance_id == agent_instance_id,
                            UserBIReport.bi_report_id == BIReport.idx,
                        ],
                    ),
                ],
                group_by_column=[BIReport.idx],
                having=[func.min(UserBIReport.status) != codes.ENABLED],
                exclude_default_filter=True,
                filters=[
                    BIReport.status == codes.ENABLED,
                ],
            )
        )
        for report in report_list:
            bi_report_id_list.append(report.idx)
            
        return bi_report_id_list
        
    def insert_reports(self, db: Session, report_list: List[dict]) -> None:
        """This method is used to insert reports

        Parameters
        ----------
        db : Session
            Session object used to insert data into database
        report_list : List[dict]
            List of reports to be inserted
        """
        self.batch_insert(db, obj_in=report_list)

    def delete_reports(self, db: Session, report_list: List[dict]) -> None:
        """This method is used to delete reports

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        report_list : List[dict]
            List of reports to be deleted
        """
        self.batch_update(db, obj_in=report_list)

    def enable_deleted_reports(self, db: Session, report_details: List[dict]) -> None:
        """This method is used to enable deleted reports

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        report_details : List[dict]
            List of reports to be enabled
        """
        self.batch_update(db, obj_in=report_details)

    def update_reports(self, db: Session, report_details: List[dict]) -> None:
        """This method is used to update reports

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        report_details : List[dict]
            List of reports data to be updated
        """
        self.batch_update(db, obj_in=report_details)


bi_report = CRUDBIReport(BIReport)
