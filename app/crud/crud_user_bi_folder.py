from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_bi_folder import UserBIFolder
from app.schemas.user_bi_folder import UserBIFolderCreate, UserBIFolderUpdate


class CRUDUserBIFolder(CRUDBase[UserBIFolder, UserBIFolderCreate, UserBIFolderUpdate]):
    def insert_folder_users(
        self, db: Session, folder_user_list: List[UserBIFolder]
    ) -> None:
        """Insert user mappings for folders

        Parameters
        ----------
        db :
            Session object used to insert data into database
        folder_user_list : List[UserBIFolder]
            List of user_bi_folder to be inserted
        """
        self.batch_insert(db, obj_in=folder_user_list)

    def delete_folder_users(self, db: Session, folder_user_list: List[dict]) -> None:
        """Delete user mappings for folders

        Parameters
        ----------
        db :
            Session object used to update data in database
        folder_user_list : List[UserBIFolder]
            List of user_bi_folder to be deleted
        """
        self.batch_update(db, obj_in=folder_user_list)

    def update_folder_users(self, db: Session, folder_user_list: List[dict]) -> None:
        """Update user mappings for folders

        Parameters
        ----------
        db :
            Session object used to update data in database
        folder_user_list : List[UserBIFolder]
            List of user_bi_folder to be updated
        """
        self.batch_update(db, obj_in=folder_user_list)


user_bi_folder = CRUDUserBIFolder(UserBIFolder)
