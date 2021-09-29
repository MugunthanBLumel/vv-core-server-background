from typing import List, cast
from sqlalchemy.sql.expression import join
from app.schemas.query import JoinModel, Model, SearchQueryModel
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session, relationship
from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
from app.schemas.bi_report import BIReportCreate,BIReportUpdate, AgentReports

class CRUDBIReports(CRUDBase[BIReport, BIReportCreate, BIReportUpdate]):
    def get_reports_by_agent_id(
        self,
        db: Session,
        *,
        agent_instance_id
    ) -> List[BIReport]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIReport.idx,
                BIReport.path,
                BIReport.guid,
                BIReport.update_hash,
                UserBIReport.agent_instance_user_id
            ],
           join=[JoinModel(model=Model(UserBIReport),
            relationship=[
                BIReport.idx == UserBIReport.bi_report_id,
                BIReport.agent_instance_id == agent_instance_id
            ])
            ],
            filters=[
                # BIReport.agent_instance_id == agent_instance_id
            ],
        )
        return cast(List[BIReport],self.get(report_search))

    def get_reports_by_agent_instance_user_id(
        self,
        db: Session,
        *,
        agent_instance_user_id
    ) -> List[AgentReports]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIReport.idx,
                BIReport.path,
                BIReport.guid,
                BIReport.update_hash,
                UserBIReport.agent_instance_user_id
            ],
            join=[JoinModel(model=Model(UserBIReport),
            relationship=[
                BIReport.idx == UserBIReport.bi_report_id,
                UserBIReport.agent_instance_user_id == agent_instance_user_id
            ])
            ]
        )
        return cast(List[AgentReports],self.get(report_search))

    

    def get_reports_by_sync_id(self,db: Session,*, sync_id: int) -> List[BIReport]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[BIReport.idx,
            BIReport.guid],
            filters=[BIReport.sync_id == sync_id,
            ]
        )
        return self.get(report_search)
    
    def create_reports(self,db, report_list: List[BIReport]) -> Session:
        self.batch_insert(db,obj_in=report_list)
        return db

    def delete_reports(self,db,report_list: List[dict]):
        return self.batch_update(db,obj_in=report_list)
    
bi_report = CRUDBIReports(BIReport)
