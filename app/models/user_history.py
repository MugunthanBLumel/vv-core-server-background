from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from app.conf import codes
from app.db.base_class import Base


class UserHistory(Base):

    __tablename__ = "user_history"  # type: ignore

    idx = Column("id", Integer, Sequence("user_history_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_type = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    viewed_at = Column(Integer, nullable=False)
    guid = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
