from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from app.conf import codes
from app.db.base import Base
from app.helpers.db_helper import DatabaseHelper


class SyncLog(Base):

    __tablename__ = "sync_log"  # type: ignore

    idx = Column("id", Integer, Sequence("sync_log_id_seq"), primary_key=True)
    
    name = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    sync_batch_id = Column(Integer, nullable=True)
    agent_instance_id = Column(Integer, ForeignKey("agent_instance.id"), nullable=True)
    meta = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    progress = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
