from typing import Dict, cast, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.agent_user import AgentUser
from app.schemas.agent_user import AgentUserCreate, AgentUserDetails, AgentUserUpdate
from app.schemas.query import SearchQueryModel


class CRUDAgentUser(CRUDBase[AgentUser, AgentUserCreate, AgentUserUpdate]):
    def get_agent_user_list(self, db: Session, agent_id: int) -> List[int]:
        """this method fetches all the agent user ids of given agent.

        Parameters
        ----------
        db : Session
            Database session object used to query the database to fetch data
        agent_id : int
            id of the agent

        Returns
        -------
        List[int]
            Contains agent user id's
        """
        agent_user: SearchQueryModel = SearchQueryModel(
            db=db,
            search_column=[AgentUser.idx],
            filters=[AgentUser.agent_id == agent_id],
        )
        return [agent_user.idx for agent_user in self.get(agent_user)]


agent_user = CRUDAgentUser(AgentUser)
