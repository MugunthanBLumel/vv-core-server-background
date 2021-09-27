from typing import Optional

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.conf import codes
from app.db.base_class import Base
from app.helpers.db_helper import DatabaseHelper


class UserFolder(Base):
    """Details of the folder which created by the user"""

    __tablename__ = "user_folder"  # type: ignore

    idx = Column("id", Integer, Sequence("user_folder_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(255), nullable=False)
    source_folder_id = Column(Integer, ForeignKey("user_folder.id"), nullable=True)
    path = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    depth = Column(Integer, nullable=False, default=1)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    parent = relationship("UserFolder", backref="sub_folder", remote_side=[idx])

    def __init__(
        self,
        name: str,
        user_id: int,
        path: str,
        depth: int,
        source_folder_id: Optional[int] = None,
        parent: Optional["UserFolder"] = None,

    ):
        self.name = name
        self.user_id = user_id
        self.path = path
        self.depth = depth
        self.created_by = user_id
        self.updated_by = user_id
        self.source_folder_id = source_folder_id
        if parent:
            self.parent = parent
