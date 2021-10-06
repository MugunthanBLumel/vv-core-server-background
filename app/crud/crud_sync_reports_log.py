from typing import List

from sqlalchemy import func
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import bindparam

from app.crud.base import CRUDBase
from app.models.sync_reports_log import SyncReportsLog
from app.schemas.query import SearchQueryModel
from app.schemas.sync_reports_log import (SyncReportsLogCreate,
                                          SyncReportsLogUpdate)


class CRUDSyncReportsLog(
    CRUDBase[SyncReportsLog, SyncReportsLogCreate, SyncReportsLogUpdate]
):
    def insert_sync_reports_log(
        self, db: Session, sync_reports_log_list: List[dict]
    ) -> None:
        """Insert List of sync reports log data in sync_reports_log table

        Parameters
        ----------
        db : Session
            Session object used to insert data into database
        sync_reports_log_list : List[dict]
            List of sync_reports_log data to be inserted
        """
        self.batch_insert(db, obj_in=sync_reports_log_list)

    def update_user_id_list(self, db: Session, user_id_update_list: List[dict]) -> None:
        """Update List of sync_reports_log data's  user_id_list in sync_reports_log table

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        user_id_update_list : List[dict]
            List of user_id_update_list data to be updated
        """
        query = (
            SyncReportsLog.__table__.update()
            .where(SyncReportsLog.__table__.c.id == bindparam("idx"))
            .values(
                {
                    "user_id_list": func.concat(
                        SyncReportsLog.__table__.c.user_id_list,
                        bindparam("user_id_list"),
                    )
                }
            )
        )

        db.execute(query, user_id_update_list)
        db.commit()

    def get_log_by_creation_time(
        self, db: Session, created_at: int, agent_instance_id: int, sync_id: int
    ) -> SyncReportsLog:
        """This method is used to get list of reports_log by creation time along with filters
           like  agent_instance_id, created_by

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        created_at : int
            time of creation of folders
        depth : int
            depth of folder's to be retrived
        agent_instance_id : int
            agent_instance_id of the folders
        created_by : into
            created_by of the folders to be retrived

        Returns
        -------
        List[BIFolder]
            List of bi_folders
        """
        sync_report_log_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[SyncReportsLog.idx, SyncReportsLog.bi_report_id],
            filters=[
                SyncReportsLog.created_at == created_at,
                SyncReportsLog.agent_instance_id == agent_instance_id,
                SyncReportsLog.sync_log_id == sync_id,
            ],
        )
        return self.get(sync_report_log_search)


sync_reports_log = CRUDSyncReportsLog(SyncReportsLog)
