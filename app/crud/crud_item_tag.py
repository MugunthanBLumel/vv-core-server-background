from typing import List

from sqlalchemy.orm.session import Session

from app.conf import codes
from app.crud.base import CRUDBase
from app.models.item_tag import ItemTag
from app.schemas.item_tag import ItemTagCreate, ItemTagUpdate


class CRUDItemTag(CRUDBase[ItemTag, ItemTagCreate, ItemTagUpdate]):
    def delete_user_report_items(
        self, db: Session, user_report_item_guid_list: List[str], user_id: int
    ) -> None:
        """This method is used to delete item_tags whose guid's in user_report_item_guid_list

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        user_report_item_guid_list : List[str]
            List of user_report_item guid's
        user_id : int
            user_id of the user performing delete
        """
        self.update(
            db,
            filters=[ItemTag.guid.in_(user_report_item_guid_list)],
            obj_in=ItemTagUpdate(status=codes.DELETED),
            user_id=user_id,
        )


item_tag = CRUDItemTag(ItemTag)
