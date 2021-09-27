from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.sql.schema import ForeignKey

from app.conf import codes
from app.db.base_class import Base
from app.helpers.db_helper import DatabaseHelper


class UserCustomUrl(Base):
    """Details of the CustomUrl which created by the user"""

    __tablename__ = "user_custom_url"  # type: ignore

    idx = Column("id", Integer, Sequence("user_custom_url_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    description = Column(DatabaseHelper.get_char_seq_type(), nullable=True)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
