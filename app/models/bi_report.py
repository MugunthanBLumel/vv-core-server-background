from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship
from app.conf import codes
from app.db.base_class import Base
from app.helpers.db_helper import DatabaseHelper


class BIReport(Base):
    """Details of the reports which fetched from the various configured agents"""

    __tablename__ = "bi_report"  # type: ignore

    idx = Column("id", Integer, Sequence("report_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    agent_instance_id = Column(Integer, nullable=False)
    bi_folder_id = Column(Integer, nullable=False)
    path = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    url = Column(DatabaseHelper.get_char_seq_type(), nullable=False)
    description = Column(DatabaseHelper.get_char_seq_type(), nullable=True)
    guid = Column(String(50), nullable=False)
    update_hash = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    