from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.agent_instance import AgentInstance
from app.schemas.agent_instance import AgentInstanceCreate, AgentInstanceUpdate


class CRUDAgentInstance(
    CRUDBase[AgentInstance, AgentInstanceCreate, AgentInstanceUpdate]
):
    def update_bi_report_count(
        self, db: Session, agent_instance_id: int, bi_report_count: int, user_id: int
    ) -> None:

        self.update(
            db,
            filters=[AgentInstance.idx == agent_instance_id],
            obj_in=AgentInstanceUpdate(bi_report_count=bi_report_count),
            user_id=user_id,
        )


agent_instance = CRUDAgentInstance(AgentInstance)
