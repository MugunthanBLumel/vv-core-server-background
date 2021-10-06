from typing import Optional

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.conf import codes
from app.db.base_class import Base
from app.helpers.db_helper import DatabaseHelper


class BIFolder(Base):
    """Maps the user and reports from various agents"""

    __tablename__ = "bi_folder"  # type: ignore

    idx = Column("id", Integer, Sequence("folder_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    source_folder_id = Column(Integer, ForeignKey("bi_folder.id"), nullable=True)
    path = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    depth = Column(Integer, nullable=False, default=1)
    agent_instance_id = Column(Integer, ForeignKey("agent_instance.id"), nullable=False)
    guid = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    parent = relationship("BIFolder", backref="sub_folder", remote_side=[idx])

    def __init__(
        self,
        name: str,
        path: str,
        depth: int,
        user_id: int,
        agent_instance_id: int,
        source_folder_id: Optional[int] = None,
        parent: Optional["BIFolder"] = None,
    ):
        self.name = name
        self.user_id = user_id
        self.path = path
        self.agent_instance_id = agent_instance_id
        self.depth = depth
        self.created_by = user_id
        self.updated_by = user_id
        self.source_folder_id = source_folder_id
        if parent:
            self.parent = parent
