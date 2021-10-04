
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
from sqlalchemy.orm import Session

from app.crud.crud_bi_folder import bi_folder
from app.api import deps
from app.api.router import TimedRoute

from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.core.sync_reports import SyncReports
from app.schemas.sync_log import SyncLogCreate
from app.schemas.sync_reports import SyncReportRequest, SyncUserReportRequest, UserDetail
import time 
import random
from app.db.session import ScopedSession
from app.models.bi_report import BIReport
from app.crud.crud_agent_instance_user import agent_instance_user
from app.crud.crud_sync_log import sync_log
from app.schemas.token import CurrentUser
from app.conf import codes

router: APIRouter = APIRouter(route_class=TimedRoute)


            
@router.post("", response_model=None)
def sync_user_reports(
    sync_report_request: SyncUserReportRequest,
    current_user: CurrentUser = Depends(deps.CurrentUser()),
    db: Session = Depends(deps.get_db)
):
    user_id: int = current_user.user_id
    sync_name: str = sync_report_request.sync_name
    for agent_instance_id in sync_report_request.agent_instance_id_list:
        agent_instance_user_id: int = current_user.agent_user_details[agent_instance_id]
        sync_id: int = sync_log.create_log(
                    db,
                    user_id=user_id,
                    sync_log_create=SyncLogCreate(
                        name = sync_name,
                        type = codes.SYNC_TYPE["admin_report_sync"],
                        agent_instance_id =agent_instance_id,
                        user_id = user_id,
                        status = codes.SYNC_STATUS["in_queue"],
                    )
                )
        sync_report_obj: SyncReports =SyncReports(sync_id=sync_id,agent_instance_id=agent_instance_id,user_id=user_id)
        user_detail: UserDetail(user_id= user_id,agent_instance_user_id= agent_instance_user_id)
        sync_report_obj.start(user_detail= user_detail)


    

