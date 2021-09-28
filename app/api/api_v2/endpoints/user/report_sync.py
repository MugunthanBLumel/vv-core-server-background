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
from app.api.api_v2.endpoints.user.report_response import get_reports
from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.core.sync_reports import SyncReports
import time 
import random
from app.db.session import ScopedSession
from app.models.bi_report import BIReport

router: APIRouter = APIRouter(route_class=TimedRoute)


@router.post("/sync", response_model=None)
def report_sync(
    db: Session = Depends(deps.get_db),
):
    SyncReports(db).sync_agent_reports()
