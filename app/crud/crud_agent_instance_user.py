from app.models.agent_instance_user import AgentInstanceUser
from typing import Dict, cast, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.agent_instance_user import AgentInstanceUser
from app.schemas.agent_instance_user import AgentInstanceUserCreate, AgentInstanceUserDetails, AgentInstanceUserUpdate
from app.schemas.query import SearchQueryModel


class CRUDAgentInstanceUser(CRUDBase[AgentInstanceUser, AgentInstanceUserCreate, AgentInstanceUserUpdate]):
    def get_agent_instance_user_list(self, db: Session, agent_instance_id: int) -> list[int]:
        """this method fetches all the agent instance user ids of given agent.

        Parameters
        ----------
        db : Session
            Database session object used to query the database to fetch data
        agent_instance_id : int
            id of the agent instance

        Returns
        -------
        list[int]
            Contains agent instance user id's
        """
        agent_instance_users: SearchQueryModel = SearchQueryModel(
            db=db,
            search_column=[AgentInstanceUser.idx],
            filters=[AgentInstanceUser.agent_instance_id == agent_instance_id],
        )
        return [agent_user.idx for agent_user in self.get(agent_instance_users)]

agent_instance_user = CRUDAgentInstanceUser(AgentInstanceUser)
