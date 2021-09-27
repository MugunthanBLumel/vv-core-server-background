from sqlalchemy import Column, ForeignKey, Integer, Sequence

from app.conf import codes
from app.db.base_class import Base


class AgentUser(Base):
    """This table maps the user and agent along with their details"""

    __tablename__ = "agent_user"  # type: ignore

    idx = Column("id", Integer, Sequence("agent_user_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agent.id"), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
