from typing import List, cast
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import join
from app.conf import codes
from app.schemas.query import JoinModel, Model, SearchQueryModel
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session, relationship
from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
from app.schemas.bi_report import BIReportCreate,BIReportUpdate, AgentReports
from itertools import chain
class CRUDBIReports(CRUDBase[BIReport, BIReportCreate, BIReportUpdate]):
    def get_reports_by_agent_id(
        self,
        db: Session,
        *,
        agent_instance_id,
        agent_instance_user_id_list: List[int]
    ) -> List[BIReport]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIReport.idx,
                BIReport.path,
                BIReport.guid,
                BIReport.update_hash,
                UserBIReport.agent_instance_user_id,
                UserBIReport.idx.label('user_bi_report_id')
            ],
           join=[JoinModel(model=Model(UserBIReport),
            relationship=[
                BIReport.idx == UserBIReport.bi_report_id,
                BIReport.agent_instance_id == agent_instance_id,
                UserBIReport.agent_instance_user_id.in_(agent_instance_user_id_list)
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
                UserBIReport.agent_instance_user_id,
                UserBIReport.idx.label('user_bi_report_id')
            ],
            join=[JoinModel(model=Model(UserBIReport),
            relationship=[
                BIReport.idx == UserBIReport.bi_report_id,
                UserBIReport.agent_instance_user_id == agent_instance_user_id
            ])
            ]
        )
        return cast(List[AgentReports],self.get(report_search))

    

    def get_reports_by_creation_time(self,db: Session,*, created_at: int) -> List[BIReport]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[BIReport.idx,
            BIReport.guid],
            filters=[
                BIReport.created_at == created_at,
            ]
        )
        return self.get(report_search)
    
    def create_reports(self,db: Session, report_list: List[BIReport]) -> Session:
        self.batch_insert(db,obj_in=report_list)
        return db

    def delete_reports(self,db: Session,report_list: List[dict]):
        return self.batch_update(db,obj_in=report_list)

    def get_existing_reports(self,db: Session,agent_instance_id: int,report_guid_list: List[str]) -> List[BIReport]:
        bi_report_list: List[BIReport] = []
        start,end = 0, len(report_guid_list)
        limit = 1000
        
        while start < end :
            slice_range: slice = slice(start, start + min(limit, end - start))
            limited_report_guid_list: List[str] = report_guid_list[slice_range]
            bi_report_list += self.get(
                    SearchQueryModel(
                    db,
                    search_column=[
                        BIReport.idx,
                        BIReport.guid,
                        BIReport.status
                    ],
                    filters=[
                        BIReport.agent_instance_id == agent_instance_id,
                        BIReport.guid.in_(limited_report_guid_list) 
                    ],
                    exclude_default_filter=True
                    )
                )
            
            start += min(limit, end - start)
        return bi_report_list

    def enable_deleted_reports(self,db: Session,report_details: List[dict]):
        self.batch_update(db,obj_in=report_details)
    
    def update_reports(self,db: Session,report_details: List[dict]):
        self.batch_update(db,obj_in=report_details)


    
bi_report = CRUDBIReports(BIReport)
