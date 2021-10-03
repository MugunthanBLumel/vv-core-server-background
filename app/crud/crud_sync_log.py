from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.sync_log import SyncLog
from app.schemas.sync_log import SyncLogCreate,SyncLogUpdate

class CRUDSyncLog(CRUDBase[SyncLog, SyncLogCreate, SyncLogUpdate]):
    def create_log(self,db: Session,user_id: int,sync_log_create: SyncLogCreate) -> SyncLog:
        return self.create(
            db,
            user_id=user_id,
            obj_in=sync_log_create
        )
        
    def update_log(self,db: Session,user_id: int,idx: int,sync_log_update: SyncLogUpdate):
        self.update(
            db=db,
            user_id=user_id,
            filters=[SyncLog.idx == idx],
            obj_in=sync_log_update
        )
        
    def get_log(self):
        pass
sync_log = CRUDSyncLog(SyncLog)