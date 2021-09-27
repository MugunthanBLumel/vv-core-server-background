from sqlalchemy import Column, ForeignKey, Integer, Sequence

from app.conf import codes
from app.db.base import Base


class ItemTag(Base):

    __tablename__ = "item_tag"  # type: ignore

    idx = Column("id", Integer, Sequence("item_tag_id_seq"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False)
    item_type = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())

    def __init__(
        self,
        tag_id: int,
        item_type: int,
        item_id: int,
        created_by: int,
        updated_by: int,
    ) -> None:
        self.tag_id = tag_id
        self.item_id = item_id
        self.item_type = item_type
        self.created_by = created_by
        self.updated_by = updated_by
