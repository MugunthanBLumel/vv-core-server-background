from sqlalchemy.orm.session import Session
from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from app.models.item_tag import ItemTag
from app.schemas.item_tag import ItemTagCreate,ItemTagUpdate
from typing import List
from app.conf import codes
class CRUDItemTag(CRUDBase[ItemTag, ItemTagCreate, ItemTagUpdate]):

    def delete_user_report_items(self,db:Session,user_report_item_guid_list: List[str], user_id: int):
        self.update(db,filters=[ItemTag.guid.in_(user_report_item_guid_list)],
        obj_in=ItemTagUpdate(
            status = codes.DELETED
        ),
        user_id=user_id
        )

        

item_tag = CRUDItemTag(ItemTag)