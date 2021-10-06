from concurrent.futures.thread import ThreadPoolExecutor

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.api.router import TimedRoute
from app.conf import codes
from app.core.sync_reports import SyncReports
from app.crud.crud_bi_report import bi_report
from app.crud.crud_sync_log import sync_log
from app.db.session import ScopedSession
from app.schemas.sync_log import SyncLogCreate
from app.schemas.sync_reports import SyncUserReportRequest, UserDetail
from app.schemas.token import CurrentUser

router: APIRouter = APIRouter(route_class=TimedRoute)


def sync(aid, uid):
    user_id: int = uid
    sync_name: str = "user sync"
    for agent_instance_id in [1]:
        db = ScopedSession()
        # agent_instance_user_id: int = current_user.agent_user_details[agent_instance_id]
        agent_instance_user_id: int = aid
        sync_id: int = sync_log.create_log(
            db,
            user_id=user_id,
            sync_log_create=SyncLogCreate(
                name=sync_name,
                type=codes.SYNC_TYPE["admin_report_sync"],
                agent_instance_id=agent_instance_id,
                user_id=user_id,
                status=codes.SYNC_STATUS["in_queue"],
            ),
        )
        db.close()
        sync_report_obj: SyncReports = SyncReports(
            sync_id=sync_id, agent_instance_id=agent_instance_id, user_id=user_id
        )
        user_detail: UserDetail = UserDetail(
            user_id=user_id, agent_instance_user_id=agent_instance_user_id
        )
        sync_report_obj.start(user_detail=user_detail)


@router.post("", response_model=None)
def sync_user_reports(
    sync_report_request: SyncUserReportRequest,
    current_user: CurrentUser = Depends(deps.CurrentUser()),
    db: Session = Depends(deps.get_db),
):

    print(bi_report.get_reports_count(db, 1))
    return
    # user_id: int = current_user.user_id
    ulist = [
        (1, 2),
        (4, 3),
        (7, 4),
        (10, 5),
        (13, 6),
        (16, 7),
        (19, 8),
        (22, 9),
        (25, 10),
        (28, 11),
        (31, 12),
        (34, 13),
        (37, 14),
        (40, 15),
        (43, 16),
        (46, 17),
        (49, 18),
        (52, 19),
        (55, 20),
        (58, 21),
        (61, 22),
        (64, 23),
        (67, 24),
        (70, 25),
        (73, 26),
        (76, 27),
        (79, 28),
        (82, 29),
        (85, 30),
        (88, 31),
        (91, 32),
        (94, 33),
        (97, 34),
        (100, 35),
        (103, 36),
        (106, 37),
        (109, 38),
        (112, 39),
        (115, 40),
        (118, 41),
        (121, 42),
        (124, 43),
        (127, 44),
        (130, 45),
        (133, 46),
        (136, 47),
        (139, 48),
        (142, 49),
        (145, 50),
        (148, 51),
    ]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(sync, task[0], task[1]): task for task in ulist}

    # user_id: int = 2
    # sync_name: str = sync_report_request.sync_name
    # for agent_instance_id in sync_report_request.agent_instance_id_list:
    #     # agent_instance_user_id: int = current_user.agent_user_details[agent_instance_id]
    #     agent_instance_user_id: int = 1
    #     sync_id: int = sync_log.create_log(
    #                 db,
    #                 user_id=user_id,
    #                 sync_log_create=SyncLogCreate(
    #                     name = sync_name,
    #                     type = codes.SYNC_TYPE["admin_report_sync"],
    #                     agent_instance_id =agent_instance_id,
    #                     user_id = user_id,
    #                     status = codes.SYNC_STATUS["in_queue"],
    #                 )
    #             )
    #     sync_report_obj: SyncReports =SyncReports(sync_id=sync_id,agent_instance_id=agent_instance_id,user_id=user_id)
    #     user_detail: UserDetail = UserDetail (user_id= user_id,agent_instance_user_id= agent_instance_user_id)
    #     sync_report_obj.start(user_detail = user_detail)
