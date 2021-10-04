from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from app.conf import codes
from app.db.base_class import Base


class UserFavorite(Base):
    """Details of the User favorited Items which can be either folder/report"""

    __tablename__ = "user_favorite"  # type: ignore

    idx = Column("id", Integer, Sequence("user_favorite_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_type = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    guid = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
