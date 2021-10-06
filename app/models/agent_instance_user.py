from sqlalchemy import Column, ForeignKey, Integer, Sequence

from app.conf import codes
from app.db.base_class import Base


class AgentInstanceUser(Base):
    """This table maps the user and agent instance along with their details"""

    __tablename__ = "agent_instance_user"  # type: ignore

    idx = Column(
        "id", Integer, Sequence("agent_instance_user_id_seq"), primary_key=True
    )
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    agent_instance_id = Column(Integer, ForeignKey("agent_instance.id"), nullable=False)
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
