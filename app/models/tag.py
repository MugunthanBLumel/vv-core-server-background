from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from app.conf import codes
from app.db.base import Base


class Tag(Base):

    __tablename__ = "tag"  # type: ignore

    idx = Column("id", Integer, Sequence("tag_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    is_admin_created = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
