from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.item_tag import ItemTag
from app.schemas.item_tag import ItemTagCreate,ItemTagUpdate
from typing import List

class CRUDItemTag(CRUDBase[ItemTag, ItemTagCreate, ItemTagUpdate]):
    def get_item_tags(self,db: Session,item_id_list: List[int],agent_instance_user_id_list: List[int]):
        item_tag_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                ItemTag.idx,
                ItemTag.item_id,
                # ItemTag
            ],
            filters=[ItemTag.item_id.in_(item_id_list)]
        )
        # self.get()

item_tag = CRUDItemTag(ItemTag)