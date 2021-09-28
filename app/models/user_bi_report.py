from sqlalchemy import Column, ForeignKey, Integer, Sequence
from sqlalchemy.orm import relationship
from app.conf import codes
from app.db.base_class import Base


class UserBIReport(Base):
    """Maps the user and reports from various agents"""

    __tablename__ = "user_bi_report"  # type: ignore

    idx = Column("id", Integer, Sequence("user_bi_report_id_seq"), primary_key=True)
    agent_instance_user_id = Column(Integer, ForeignKey("agent_instance_user.id"), nullable=False)
    bi_report_id = Column(Integer, ForeignKey("bi_report.id"), nullable=True)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    