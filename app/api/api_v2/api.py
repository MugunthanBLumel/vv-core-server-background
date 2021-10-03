""" API Router Configuration """
from fastapi import APIRouter

from app.api.router import TimedRoute
from app.api.api_v2.endpoints.user import sync_reports as sync_user_reports
from app.api.api_v2.endpoints.admin import sync_reports

# Router init
v2_api_router = APIRouter(route_class=TimedRoute)

# All future routers needs to be included like below

v2_api_router.include_router(
     sync_reports.router, prefix="/admin/sync/report", tags=["Sync Reports"]
 )

v2_api_router.include_router(
     sync_user_reports.router, prefix="/user/sync/report", tags=["Sync User Reports"]
 )

