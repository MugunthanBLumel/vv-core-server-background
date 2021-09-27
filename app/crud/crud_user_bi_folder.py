from typing import List
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.user_bi_folder import UserBIFolderCreate,UserBIFolderUpdate
from app.models.user_bi_folder import UserBIFolder
from app.schemas.query import JoinModel, SearchQueryModel,Model
from time import time
from app.db.session import engine
class CRUDUserBIFolder(CRUDBase[UserBIFolder, UserBIFolderCreate, UserBIFolderUpdate]):
    def get_bi_folder_user_mapping(
        self,
        db: Session,
        *,
        agent_user_id_list: List[int]
    ) -> List[UserBIFolder]:
        bi_folder_user_mapping_list: List[UserBIFolder] = []
        
        start,end = 0, len(agent_user_id_list)
        limit = 1000
        while start < end :
            slice_range: slice = slice(start, start + min(limit, end - start))
            
            limited_agent_user_id_list: List[int] = agent_user_id_list[slice_range]
            
            bi_folder_user_mapping_list += self.get(
                    SearchQueryModel(
                    db,
                    search_column=[UserBIFolder.bi_folder_id,UserBIFolder.agent_user_id,
                    UserBIFolder.report_count],
                    filters=[UserBIFolder.agent_user_id.in_(limited_agent_user_id_list)],
                    )
                )
            
            start += min(limit, end - start)
        return bi_folder_user_mapping_list
    def insert_folder_users(self,db, folder_user_list: List[UserBIFolder]):
        self.batch_insert(db,obj_in=folder_user_list)
user_bi_folder = CRUDUserBIFolder(UserBIFolder)