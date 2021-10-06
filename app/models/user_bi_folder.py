from sqlalchemy import Column, ForeignKey, Integer, Sequence

from app.conf import codes
from app.db.base_class import Base


class UserBIFolder(Base):
    """Mapping between the AgentInstanceUser and BI Folder to define the user accessibility"""

    __tablename__ = "user_bi_folder"  # type: ignore

    idx = Column("id", Integer, Sequence("user_bi_folder_seq"), primary_key=True)
    agent_instance_user_id = Column(
        Integer, ForeignKey("agent_instance_user.id"), nullable=False
    )
    bi_folder_id = Column(Integer, ForeignKey("bi_folder.id"), nullable=False)
    bi_report_count = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
