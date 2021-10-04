from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from app.conf import codes
from app.db.base import Base
from app.helpers.db_helper import DatabaseHelper

class SyncReportsLog(Base):

    __tablename__ = "sync_reports_log"  # type: ignore

    idx = Column("id", Integer, Sequence("sync_reports_log_id_seq"), primary_key=True)
    sync_log_id = Column(Integer, nullable=False)
    agent_instance_id = Column(Integer, ForeignKey("agent_instance.id"), nullable=False)
    bi_report_id = Column(Integer,ForeignKey("bi_report.id"), nullable=False )
    user_id_list = Column(DatabaseHelper.get_long_char_seq_type(), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
