
from app.schemas.bi_folder import AgentFolders
from app.models.bi_folder import BIFolder
from app.models.user_folder import UserFolder
from sqlalchemy.sql.functions import random
from app.schemas.query import SearchQueryModel
from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
from app.schemas.bi_report import AgentReports
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from loguru import logger
from sqlalchemy.orm import Session, session

from app.crud.crud_bi_folder import bi_folder
from app.api import deps
from app.api.router import TimedRoute

from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.core.sync_reports import SyncReports
import time 
import random
from app.db.session import ScopedSession
from app.models.bi_report import BIReport
from app.crud.crud_agent_instance_user import agent_instance_user
router: APIRouter = APIRouter(route_class=TimedRoute)

def update(
        db: Session,
        filters = [],
        commit: bool = True,
        *,
        obj_in,
        user_id: int,
    ) -> None:
        """updates existing records which matches the provided filter,
        updates all record if filter is empty

        Parameters
        ----------
        db : Session
            Database session object
        obj_in : Union[ UpdateSchemaType,
                 Dict[str, GenericFunction],
                 Dict[Column, GenericFunction], ]
            data to be updated or generic function that will return dynamic data
            to update
        filters : List[ColumnElement], optional
            filter to perform update for, by default []
        commit : bool, optional
             flag to skip commit, by default True
        user_id : int
             user_id of the user performing update
        Raises
        ------
            Raises DbException and the transaction is rolledback
        """
        
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db.query(BIReport).filter(*filters).update(
            {
                **update_data,
                "updated_at": str(int(time.time())),
                "updated_by": user_id,
            },
            synchronize_session=False,
        )
        if commit:
            db.commit()
       
# def test_update():
#     t1=time.time()
#     for i in range(100):
        


            
@router.post("/sync", response_model=None)
def report_sync(
    db: Session = Depends(deps.get_db),
):
    for i in db.query(BIReport).filter(BIReport.idx == [1,2]).all():
        print(i)
    # SyncReports(db).sync_agent_instance_reports()
    # SyncReports(db).sync_agent_instance_reports()
    pass

    
