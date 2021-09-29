
from app.models.user_bi_folder import UserBIFolder
from app.schemas.bi_folder import AgentFolders, BIFolderCreate, BIFolderUpdate
from app.models.bi_folder import BIFolder
from typing import List, cast

from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.db.session import SessionLocal,ScopedSession

from app.crud.crud_user_bi_folder import user_bi_folder


class CRUDBIFolder(CRUDBase[BIFolder, BIFolderCreate, BIFolderUpdate]):
   
    
    def get_folders_by_agent_id(
        self,
        db: Session,
        *,
        agent_instance_id
    ) -> List[AgentFolders]:
        
        
        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIFolder.idx,
                BIFolder.guid,
                UserBIFolder.agent_instance_user_id,
                UserBIFolder.bi_report_count
            ],
            join=[
            JoinModel(model=Model(UserBIFolder),
            relationship=[
                BIFolder.idx == UserBIFolder.bi_folder_id,
                BIFolder.agent_instance_id == agent_instance_id
            ])
            ],
            filters=[BIFolder.agent_instance_id == agent_instance_id]

        )
        
        # for report in self.get(report_search):
        #     agent_folder_list.append(AgentFolders(

        #     ))
        return cast(List[AgentFolders],self.get(folder_search))

    def get_folders_by_agent_instance_user_id(
        self,
        db: Session,
        *,
        agent_instance_user_id
    ) -> List[AgentFolders]:
        report_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIFolder.idx,
                BIFolder.guid,
                UserBIFolder.agent_instance_user_id,
                UserBIFolder.bi_report_count
            ],
            join=[JoinModel(model=Model(UserBIFolder),
            relationship=[
                BIFolder.idx == UserBIFolder.bi_folder_id,
                UserBIFolder.agent_instance_user_id == agent_instance_user_id
            ])
            ]
        )
        return cast(List[AgentFolders],self.get(report_search))

    def get_folders_by_sync_id(self,db: Session,*, sync_id: int, depth: int) -> List[BIFolder]:
        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[BIFolder.idx,
            BIFolder.guid],
            filters=[BIFolder.sync_id == sync_id,
            BIFolder.depth == depth
            ]
        )
        return self.get(folder_search)
    
    def create_folders(self,db,folder_list: List[dict]):
        return self.batch_insert(db,obj_in = folder_list)

    def delete_folders(self,db,folder_list: List[dict]):
        return self.batch_update(db,obj_in=folder_list)
    

bi_folder = CRUDBIFolder(BIFolder)
