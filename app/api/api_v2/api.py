""" API Router Configuration """
from fastapi import APIRouter

from app.api.router import TimedRoute
from app.api.api_v2.endpoints.user import report_sync
# Router init
v2_api_router = APIRouter(route_class=TimedRoute)

# All future routers needs to be included like below
v2_api_router.include_router(
     report_sync.router, prefix="/user/report_sync", tags=["Report Sync"]
 )
