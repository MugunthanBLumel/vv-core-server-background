from sqlalchemy.orm.session import Session

from app.crud.base import CRUDBase
from app.models.sync_log import SyncLog
from app.schemas.query import SearchQueryModel
from app.schemas.sync_log import SyncLogCreate, SyncLogUpdate


class CRUDSyncLog(CRUDBase[SyncLog, SyncLogCreate, SyncLogUpdate]):
    def create_log(
        self, db: Session, user_id: int, sync_log_create: SyncLogCreate
    ) -> int:
        """This method is used to create a sync log entry in the sync_log table

        Parameters
        ----------
        db : Session
            Session object used to insert data into database
        user_id : int
            user_id of the user performing create
        sync_log_create : SyncLogCreate
            details of sync log to be created

        Returns
        -------
        int
            idx of the sync log created
        """
        return self.create(db, user_id=user_id, obj_in=sync_log_create).idx

    def update_log(
        self, db: Session, user_id: int, idx: int, sync_log_update: SyncLogUpdate
    ) -> None:
        """This method is used to update a sync log entry

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        user_id : int
            user_id of the user performing update
        idx : int
            idx of the record in sync_log table
        sync_log_update : SyncLogUpdate
            details of sync log to be updated
        """
        self.update(
            db=db, user_id=user_id, filters=[SyncLog.idx == idx], obj_in=sync_log_update
        )

    def get_sync_status(self, db: Session, idx: int) -> int:
        """This method is used to get status of current sync

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        sync_id : int
            idx of the sync
        Returns
        -------
        int
            status of the sync
        """
        return self.get_first(
            SearchQueryModel(
                db, search_column=[SyncLog.status], filters=[SyncLog.idx == idx]
            )
        ).status


sync_log = CRUDSyncLog(SyncLog)
