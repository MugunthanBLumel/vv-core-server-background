from datetime import datetime
from typing import Dict, TypedDict

from pydantic import validator
from pydantic.main import BaseModel


class UserTokenInfo(TypedDict):
    user_id: int
    agent_user_details: Dict[int, int]


class CurrentUser(BaseModel):
    user_id: int
    agent_user_details: Dict[
        int, int
    ]  # Mapping between AgentId and AgentUserId of the User

    @validator("agent_user_details")
    def convert_agent_user_details(cls, value: Dict[str, int]) -> Dict:
        """Convert the key agent_id to integer in agent user details

        Parameters
        ----------
        value : Dict[str, int]
            User accessible agent details

        Returns
        -------
        Dict[int, int]
            Agent details where agent_id as key and agent_user_id as value
        """
        return {
            int(agent_id): agent_user_id for agent_id, agent_user_id in value.items()
        }


class TokenEncoder(TypedDict):
    exp: datetime
    user_identity: UserTokenInfo
