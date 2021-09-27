from sqlalchemy import Column, Integer, Sequence, String

from app.conf import codes
from app.db.base_class import Base


class Agent(Base):
    """This table contains the configuration details of the added agent"""

    __tablename__ = "agent"  # type: ignore

    idx = Column("id", Integer, Sequence("agent_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
