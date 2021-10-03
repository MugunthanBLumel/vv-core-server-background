from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.user_report import UserReport
from app.schemas.user_report import UserReportCreate,UserReportUpdate

class CRUDUserReport(CRUDBase[UserReport, UserReportCreate, UserReportUpdate]):
    pass

user_report = CRUDUserReport(UserReport)