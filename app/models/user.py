from sqlalchemy import Column, Integer, Sequence, String

from app.conf import codes
from app.db.base_class import Base


class User(Base):
    """Details of the unique user who logged into BI Hub"""

    __tablename__ = "user"  # type: ignore

    id = Column("id", Integer, Sequence("user_id_seq"), primary_key=True)
    fullname = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
