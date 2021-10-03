from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.user_history import UserHistory
from app.schemas.user_history import UserHistoryCreate,UserHistoryUpdate

class CRUDItemTag(CRUDBase[UserHistory, UserHistoryCreate, UserHistoryUpdate]):
    pass

user_history = CRUDItemTag(UserHistory)