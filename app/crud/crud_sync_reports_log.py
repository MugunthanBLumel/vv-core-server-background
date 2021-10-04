from sqlalchemy.orm.session import Session
from typing import List
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.sync_reports_log import SyncReportsLog
from app.schemas.sync_reports_log import SyncReportsLogCreate,SyncReportsLogUpdate
from sqlalchemy.sql.expression import bindparam
from sqlalchemy import func

class CRUDSyncReportsLog(CRUDBase[SyncReportsLog, SyncReportsLogCreate, SyncReportsLogUpdate]):
    
    def insert_sync_reports_log(self,db: Session, sync_reports_log_list: List[dict]) -> Session:
        return self.batch_insert(db, obj_in= sync_reports_log_list)
    
    def update_sync_reports_log(self,db: Session, sync_reports_log_list: List[dict]) -> Session:
        return self.batch_update(db, obj_in= sync_reports_log_list)

    def update_user_id_list(self, db: Session, user_id_update_list: List[dict]):
        query = SyncReportsLog.__table__.update().\
        where(SyncReportsLog.__table__.c.id == bindparam('idx')).\
        values(
        {
            'user_id_list': func.concat(SyncReportsLog.__table__.c.user_id_list,bindparam('user_id_list'))
        }
        )

        db.execute(query, user_id_update_list)
        db.commit()
        
    def get_log_by_creation_time(self,db: Session, created_at: int, agent_instance_id: int, sync_id: int):
        sync_report_log_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                SyncReportsLog.idx,
                SyncReportsLog.bi_report_id
            ],
            filters=[
                SyncReportsLog.created_at == created_at,
                SyncReportsLog.agent_instance_id == agent_instance_id,
                SyncReportsLog.sync_log_id == sync_id
            ]
        )
        return self.get(sync_report_log_search)
        
sync_reports_log = CRUDSyncReportsLog(SyncReportsLog)