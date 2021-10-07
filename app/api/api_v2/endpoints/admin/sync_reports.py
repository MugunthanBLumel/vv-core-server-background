from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.api.router import TimedRoute
from app.conf import codes
from app.core.sync_reports import SyncReports
from app.crud.crud_sync_log import sync_log
from app.db.session import ScopedSession
from app.schemas.sync_log import SyncLogCreate, SyncLogUpdate
from app.schemas.sync_reports import SyncReportRequest
from app.schemas.token import CurrentUser

router: APIRouter = APIRouter(route_class=TimedRoute)


@router.post("", response_model=None)
def sync_reports(
    sync_report_request: SyncReportRequest,
    current_user: CurrentUser = Depends(deps.CurrentUser()),
    
):
    db= ScopedSession()
    user_id: int = 1
    sync_name: str = sync_report_request.sync_name
    sync_batch_id: Optional[int] = None

    sync_batch_id = sync_log.create_log(
        db,
        user_id,
        SyncLogCreate(
            name=sync_name,
            type=codes.SYNC_TYPE["admin_report_sync"],
            user_id=user_id,
            status=codes.SYNC_STATUS["in_queue"],
        ),
    )

    sync_log.update_log(
        db,
        user_id=user_id,
        idx=sync_batch_id,
        sync_log_update=SyncLogUpdate(
            start_time=codes.DEFAULT_TIME(),
            status=codes.SYNC_STATUS["started"],
        ),
    )
    for agent_instance_id in sync_report_request.agent_instance_id_list:
        sync_id: int = sync_log.create_log(
            db,
            user_id=user_id,
            sync_log_create=SyncLogCreate(
                name=sync_name,
                type=codes.SYNC_TYPE["admin_report_sync"],
                sync_batch_id=sync_batch_id,
                agent_instance_id=agent_instance_id,
                user_id=user_id,
                status=codes.SYNC_STATUS["in_queue"],
            ),
        )
        sync_report_obj: SyncReports = SyncReports(
            db,
            sync_id=sync_id, agent_instance_id=agent_instance_id, user_id=user_id
        )
        sync_report_obj.start()

    sync_log.update_log(
        db,
        user_id=user_id,
        idx=sync_batch_id,
        sync_log_update=SyncLogUpdate(
            end_time=codes.DEFAULT_TIME(),
            status=codes.SYNC_STATUS["success"],
        ),
    )
    db.close()