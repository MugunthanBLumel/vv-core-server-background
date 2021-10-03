
from sqlalchemy.sql.elements import ColumnElement
from app.models.user_bi_folder import UserBIFolder
from app.schemas.bi_folder import AgentFolders, BIFolderCreate, BIFolderUpdate
from app.models.bi_folder import BIFolder
from typing import List, cast

from app.schemas.query import JoinModel, SearchQueryModel,Model
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.db.session import SessionLocal,ScopedSession

from app.crud.crud_user_bi_folder import user_bi_folder
from app.conf import codes
from itertools import chain

class CRUDBIFolder(CRUDBase[BIFolder, BIFolderCreate, BIFolderUpdate]):
   
    
    def get_folders_by_agent_id(
        self,
        db: Session,
        *,
        agent_instance_id: int,
        agent_instance_user_id_list: List[int]
    ) -> List[AgentFolders]:
        
        
        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIFolder.idx,
                BIFolder.guid,
                UserBIFolder.agent_instance_user_id,
                UserBIFolder.bi_report_count,
                UserBIFolder.idx.label('user_bi_folder_id')
            ],
            join=[
            JoinModel(model=Model(UserBIFolder),
            relationship=[
                BIFolder.idx == UserBIFolder.bi_folder_id,
                BIFolder.agent_instance_id == agent_instance_id,
                UserBIFolder.agent_instance_user_id.in_(agent_instance_user_id_list)
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
        agent_instance_user_id: int
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

    def get_folders_by_creation_time(self,db: Session,*, created_at: int, depth: int) -> List[BIFolder]:
        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIFolder.idx,
            BIFolder.guid],
            filters=[
                BIFolder.depth == depth,
                BIFolder.created_at == created_at
            ]
        )
        return self.get(folder_search)
    
    def create_folders(self,db,folder_list: List[dict]):
        return self.batch_insert(db,obj_in = folder_list)

    def delete_folders(self,db,folder_list: List[dict]):
        return self.batch_update(db,obj_in=folder_list)
    
    def get_folders_by_guid(self,db: Session,agent_instance_id: int,folder_guid_list: List[str]
    ) -> List[BIFolder]:
        bi_folder_list: List[BIFolder] = []
        start,end = 0, len(folder_guid_list)
        limit = 1000
        while start < end :
            slice_range: slice = slice(start, start + min(limit, end - start))
            limited_folder_guid_list: List[str] = folder_guid_list[slice_range]
            bi_folder_list += self.get(
                    SearchQueryModel(
                    db,
                    search_column=[
                        BIFolder.idx,
                        BIFolder.guid,
                        BIFolder.status
                        ],
                    filters=[
                        BIFolder.agent_instance_id == agent_instance_id,
                        BIFolder.guid.in_(limited_folder_guid_list) 
                    ],
                    exclude_default_filter=True
                    )
                )
            
            start += min(limit, end - start)
        return bi_folder_list

    def enable_deleted_folders(self,db: Session,folder_details: List[dict]):
        self.batch_update(db,obj_in=folder_details)

bi_folder = CRUDBIFolder(BIFolder)
