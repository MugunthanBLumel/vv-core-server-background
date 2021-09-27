from typing import List
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.user_bi_report import UserBIReportCreate,UserBIReportUpdate
from app.models.user_bi_report import UserBIReport
from app.schemas.query import JoinModel, SearchQueryModel,Model
from time import time
from app.db.session import engine
class CRUDUserBIReport(CRUDBase[UserBIReport, UserBIReportCreate, UserBIReportUpdate]):
    def get_bi_report_user_mapping(
        self,
        db: Session,
        *,
        agent_user_id_list: List[int]
    ) -> List[UserBIReport]:
        bi_report_user_mapping_list: List[UserBIReport] = []
        
        start,end = 0, len(agent_user_id_list)
        limit = 1000
        while start < end :
            slice_range: slice = slice(start, start + min(limit, end - start))
            
            limited_agent_user_id_list: List[int] = agent_user_id_list[slice_range]
            
            bi_report_user_mapping_list += self.get(
                    SearchQueryModel(
                    db,
                    search_column=[UserBIReport.report_id,UserBIReport.agent_user_id],
                    filters=[UserBIReport.agent_user_id.in_(limited_agent_user_id_list)],
                    )
                )
            
            start += min(limit, end - start)
        return bi_report_user_mapping_list
    
    def insert_report_users(self,db, report_user_list: List[UserBIReport]):
        self.batch_insert(db,obj_in=report_user_list)
user_bi_report = CRUDUserBIReport(UserBIReport)