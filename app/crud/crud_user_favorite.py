from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.user_favorite import UserFavorite
from app.schemas.user_favorite import UserFavoriteCreate,UserFavoriteUpdate

class CRUDItemTag(CRUDBase[UserFavorite, UserFavoriteCreate, UserFavoriteUpdate]):
    pass

item_tag = CRUDItemTag(UserFavorite)