from typing import List, cast

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.conf import codes
from app.crud.base import CRUDBase
from app.models.bi_folder import BIFolder
from app.models.user_bi_folder import UserBIFolder
from app.schemas.bi_folder import (BIFolderCreate, BIFolderDetails,
                                   BIFolderUpdate)
from app.schemas.query import JoinModel, Model, SearchQueryModel


class CRUDBIFolder(CRUDBase[BIFolder, BIFolderCreate, BIFolderUpdate]):
    def get_folders(
        self,
        db: Session,
        *,
        agent_instance_id: int,
        agent_instance_user_id_list: List[int]
    ) -> List[BIFolderDetails]:
        """This method is used to get list of bi_folders along with its user mapping

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id of the folders to be fetched
        agent_instance_user_id_list : List[int]
            agent_instance_user_id_list who's folders will be fetched

        Returns
        -------
        List[BIFolderDetails]
            List of bi_folders and user_mapping details
        """

        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[
                BIFolder.idx,
                BIFolder.guid,
                UserBIFolder.agent_instance_user_id,
                UserBIFolder.bi_report_count,
                UserBIFolder.idx.label("user_bi_folder_id"),
            ],
            join=[
                JoinModel(
                    model=Model(UserBIFolder),
                    relationship=[
                        BIFolder.idx == UserBIFolder.bi_folder_id,
                        BIFolder.agent_instance_id == agent_instance_id,
                        UserBIFolder.agent_instance_user_id.in_(
                            agent_instance_user_id_list
                        ),
                    ],
                )
            ],
            filters=[BIFolder.agent_instance_id == agent_instance_id],
        )

        return cast(List[BIFolderDetails], self.get(folder_search))

    def get_folders_by_creation_time(
        self,
        db: Session,
        *,
        created_at: int,
        depth: int,
        agent_instance_id: int,
        created_by: int
    ) -> List[BIFolder]:
        """This method is used to get list of bi_folders by creation time along with filters
           like  depth, agent_instance_id, created_by

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        created_at : int
            time of creation of folders
        depth : int
            depth of folder's to be retrived
        agent_instance_id : int
            agent_instance_id of the folders
        created_by : into
            created_by of the folders to be retrived

        Returns
        -------
        List[BIFolder]
            List of bi_folders
        """
        folder_search: SearchQueryModel = SearchQueryModel(
            db,
            search_column=[BIFolder.idx, BIFolder.guid],
            filters=[
                BIFolder.depth == depth,
                BIFolder.created_at == created_at,
                BIFolder.agent_instance_id == agent_instance_id,
                BIFolder.created_by == created_by,
            ],
        )
        return self.get(folder_search)

    def get_folders_by_guid(
        self, db: Session, agent_instance_id: int, folder_guid_list: List[str]
    ) -> List[BIFolder]:
        """This method is used to get list of bi_folders by folder_guid_list including deleted folders

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id of the folders
        folder_guid_list : List[str]
            List of guid's of the folders to be retrived

        Returns
        -------
        List[BIFolder]
            List of bi_folders
        """
        bi_folder_list: List[BIFolder] = []
        start: int = 0
        end: int = len(folder_guid_list)
        limit: int = 1000
        while start < end:
            slice_range: slice = slice(start, start + min(limit, end - start))
            limited_folder_guid_list: List[str] = folder_guid_list[slice_range]
            bi_folder_list += self.get(
                SearchQueryModel(
                    db,
                    search_column=[BIFolder.idx, BIFolder.guid, BIFolder.status],
                    filters=[
                        BIFolder.agent_instance_id == agent_instance_id,
                        BIFolder.guid.in_(limited_folder_guid_list),
                    ],
                    exclude_default_filter=True,
                )
            )

            start += min(limit, end - start)
        return bi_folder_list

    def get_folders_to_be_deleted(
        self, db: Session, agent_instance_id: int, folder_id_list: List[int]
    ) -> List[int]:
        """This method is used to get list of non deleted folder id's
        which doesn't have user mappings

        Parameters
        ----------
        db : Session
            Session object used to retrive data from database
        agent_instance_id : int
            agent_instance_id's of the folder
        folder_id_list : int
            list of folder id's
        Returns
        -------
        List[int]
            list of non deleted folder id's which doesn't have user mappings
        """
        bi_folder_id_list: List[int] = []
        start: int = 0
        end: int = len(folder_id_list)
        limit: int = 1000

        while start < end:
            slice_range: slice = slice(start, start + min(limit, end - start))
            limited_folder_id_list: List[int] = folder_id_list[slice_range]
            folder_list: List[BIFolder] = self.get(
                SearchQueryModel(
                    db,
                    search_column=[BIFolder.idx],
                    join=[
                        JoinModel(
                            model=Model(UserBIFolder),
                            relationship=[
                                BIFolder.agent_instance_id == agent_instance_id,
                                UserBIFolder.bi_folder_id == BIFolder.idx,
                            ],
                        ),
                    ],
                    group_by_column=[BIFolder.idx],
                    having=[func.min(UserBIFolder.status) != codes.ENABLED],
                    exclude_default_filter=True,
                    filters=[
                        BIFolder.idx.in_(limited_folder_id_list),
                        BIFolder.status == codes.ENABLED,
                    ],
                )
            )
            for folder in folder_list:
                bi_folder_id_list.append(folder.idx)
            start += min(limit, end - start)
        return bi_folder_id_list

    def insert_folders(self, db: Session, folder_list: List[dict]) -> None:
        """This method is used to insert folders

        Parameters
        ----------
        db : Session
            Session object used to insert data into database
        folder_list : List[dict]
            List of folders to be inserted
        """
        self.batch_insert(db, obj_in=folder_list)

    def delete_folders(self, db: Session, folder_list: List[dict]) -> None:
        """This method is used to delete folders

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        folder_list : List[dict]
            List of folders to be deleted
        """
        self.batch_update(db, obj_in=folder_list)

    def enable_deleted_folders(self, db: Session, folder_details: List[dict]) -> None:
        """This method is used to enable deleted folders

        Parameters
        ----------
        db : Session
            Session object used to update data in database
        folder_details : List[dict]
            List of folders to be enabled
        """
        self.batch_update(db, obj_in=folder_details)


bi_folder = CRUDBIFolder(BIFolder)
