import json
from hashlib import sha1
from typing import List, Optional, Tuple

from loguru import logger
from sqlalchemy.orm.session import Session

from app.api.api_v2.endpoints.user.report_response import get_reports
from app.conf import codes
from app.core.exception import StopSyncException
from app.crud.crud_agent_instance import agent_instance
from app.crud.crud_agent_instance_user import agent_instance_user
from app.crud.crud_bi_folder import bi_folder
from app.crud.crud_bi_report import bi_report
from app.crud.crud_item_tag import item_tag
from app.crud.crud_sync_log import sync_log
from app.crud.crud_sync_reports_log import sync_reports_log
from app.crud.crud_user_bi_folder import user_bi_folder
from app.crud.crud_user_bi_report import user_bi_report
from app.crud.crud_user_favorite import user_favorite
from app.crud.crud_user_history import user_history
from app.crud.crud_user_report import user_report
from app.models.bi_folder import BIFolder
from app.models.bi_report import BIReport
from app.models.sync_reports_log import SyncReportsLog
from app.schemas.bi_folder import BIFolderDetails
from app.schemas.bi_report import BIReportDetails
from app.schemas.sync_log import SyncLogUpdate
from app.schemas.sync_reports import (ExistingFolder, ExistingReport,
                                      FolderReportCountUpdate,
                                      FolderUserDetails, IncomingFolder,
                                      IncomingReport, UserDetail)
from time import time

class SyncReports:
    def __init__(
        self, db: Session, sync_id: int, agent_instance_id: int, user_id: int
    ) -> None:
        """SyncReports init function used to initialise variables

        Parameters
        ----------
        db : Session
            Session object used to perform crud operations in database
        sync_id : int
            sync_id of sync
        agent_instance_id : int
            agent_instance id
        user_id : int
            user_id of the user performing sync
        """
        self.db: Session = db
        self.progress: int = 0
        self.sync_id: int = sync_id
        self.agent_instance_id: int = agent_instance_id
        self.user_id: int = user_id
        self.is_admin_sync: bool = False
        self.agent_instance_user_id_map: dict[
            int, int
        ] = {}  # agent_instance_user_id: user_id
        self.agent_instance_user_id_batch_list: list[
            int
        ] = []  # list of agent_instance_user_id of the batch

        self.incoming_report_map: dict[
            str, IncomingReport
        ] = {}  # report guid: IncomingReport
        self.incoming_folder_map: dict[
            str, IncomingFolder
        ] = {}  # folder guid: IncomingFolder
        self.existing_report_map: dict[
            str, ExistingReport
        ] = {}  # report guid: ExistingReport
        self.existing_folder_map: dict[
            str, ExistingFolder
        ] = {}  # folder guid: ExistingFolder
        self.report_id_log_id_map: dict[int, int] = {}  # report id: sync_reports_log id

        self.reports_to_be_inserted: List[str] = []  # list of report_guid
        self.folders_to_be_inserted: dict[
            int, List[str]
        ] = {}  # depth: list of folder guid of the depth
        self.report_user_mapping_to_be_inserted: dict[
            int, List[str]
        ] = {}  # agent_instance_user_id: list(report guid)
        self.folder_user_mapping_to_be_inserted: dict[
            int, List[str]
        ] = {}  # agent_instance_user_id: list(folder guid)
        self.sync_reports_log_to_be_inserted: dict[
            int, dict
        ] = {}  # report id: sync_reports_log details

        self.reports_to_be_updated: List[dict] = []  # list of report details
        self.folder_user_report_count_update: List[FolderReportCountUpdate] = []
        self.sync_reports_log_to_be_updated: dict[
            int, dict
        ] = {}  # report id: user_id_list to be updated

        self.batch_reports_to_be_deleted: set[int] = set()  # set of report_id's
        self.batch_folders_to_be_deleted: set[int] = set()  # set of folder_id's
        self.report_user_mapping_to_be_deleted: List[
            int
        ] = []  # list of user_bi_report id's
        self.folder_user_mapping_to_be_deleted: List[
            int
        ] = []  # list of user_folder id's
        self.user_report_item_guid_to_be_deleted: List[
            str
        ] = []  # list of guid used to delete report reference in other tables

    def generate_incoming_report_folder_aggregate(
        self, *, incoming_report_details: List[Tuple[int, dict]]
    ) -> None:
        """This method is used to construct incoming report and folder aggregate

        Parameters
        ----------
        incoming_report_details : List[Tuple[int,dict]]
            incoming report response (agent_instance_user_id: Incoming report response)
        """
        logger.debug(
            f"Starting to generate incoming report and folder aggregate for the sync_id {self.sync_id}"
        )
        incoming_report_map: dict[str, IncomingReport] = {}
        incoming_folder_map: dict[str, IncomingFolder] = {}
        for agent_instance_user_id, incoming_reports in incoming_report_details:
            added_folder_guid = set()
            for incoming_report in incoming_reports:
                incoming_report_guid: str = sha1(
                    "_".join(
                        [
                            incoming_report["report_id"],
                            str(self.agent_instance_id),
                            incoming_report["path"],
                        ]
                    ).encode()
                ).hexdigest()
                incoming_report_obj: IncomingReport = incoming_report_map.get(
                    incoming_report_guid
                )
                # Creating report aggregate(incoming_report_map) based on report guid
                if incoming_report_obj:
                    incoming_report_obj.agent_instance_users.append(
                        agent_instance_user_id
                    )
                else:
                    meta: str = json.dumps(incoming_report["meta"])
                    sync_meta: str = json.dumps(incoming_report["sync_metadata"])
                    update_hash: str = sha1(
                        "_".join(
                            [
                                incoming_report["name"],
                                incoming_report["description"],
                                incoming_report["url"],
                                meta,
                                sync_meta,
                            ]
                        ).encode()
                    ).hexdigest()

                    incoming_report_map[incoming_report_guid] = IncomingReport(
                        name=incoming_report["name"],
                        description=incoming_report["description"],
                        report_id=incoming_report["report_id"],
                        url=incoming_report["url"],
                        url_t=incoming_report["url_t"],
                        path=incoming_report["path"],
                        meta=meta,
                        sync_metadata=sync_meta,
                        agent_instance_users=[agent_instance_user_id],
                        guid=incoming_report_guid,
                        update_hash=update_hash,
                    )
                # Creating folder aggregate(incoming_report_map) based on folder guid
                report_folder_path_list: str = (
                    incoming_report["path"]
                    .rstrip(codes.path_delimiter)
                    .split(codes.path_delimiter)
                )
                for index, folder_name in enumerate(reversed(report_folder_path_list)):
                    depth: int = len(report_folder_path_list) - index
                    folder_path: str = (
                        codes.path_delimiter.join(report_folder_path_list[:depth])
                        + codes.path_delimiter
                    )
                    folder_guid: str = sha1(
                        "_".join([str(self.agent_instance_id), folder_path]).encode()
                    ).hexdigest()

                    incoming_folder: IncomingFolder = incoming_folder_map.get(
                        folder_guid
                    )
                    if not incoming_folder:
                        user_report_count: int = 1 if index == 0 else 0
                        incoming_folder_map[folder_guid] = IncomingFolder(
                            name=folder_name,
                            path=folder_path,
                            agent_instance_id=self.agent_instance_id,
                            depth=depth,
                            guid=folder_guid,
                            agent_instance_users=[agent_instance_user_id],
                            user_report_count_map={
                                agent_instance_user_id: user_report_count
                            },
                        )
                    else:
                        if folder_guid not in added_folder_guid:
                            incoming_folder.agent_instance_users.append(
                                agent_instance_user_id
                            )
                        if index == 0:
                            incoming_folder.user_report_count_map[
                                agent_instance_user_id
                            ] = (
                                incoming_folder.user_report_count_map.get(
                                    agent_instance_user_id, 0
                                )
                                + 1
                            )
                        else:
                            incoming_folder.user_report_count_map[
                                agent_instance_user_id
                            ] = 0
                    added_folder_guid.add(folder_guid)

        self.incoming_report_map = incoming_report_map
        self.incoming_folder_map = incoming_folder_map
        
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        
        logger.debug(
            f"Incoming report and folder aggregate generated successfully for the sync_id {self.sync_id}"
        )
        self.check_running_status()

    def generate_existing_report_aggregate(self) -> None:
        """This method is used to construct existing report aggregate"""
        logger.debug(
            f"Starting to generate existing report aggregate for the sync_id {self.sync_id}"
        )
        existing_report_map: dict[str, ExistingReport] = {}
        logger.debug(
            f"Getting existing reports from db for the sync_id {self.sync_id}..."
        )
        existing_report_list: List[BIReportDetails] = bi_report.get_reports(
            self.db,
            agent_instance_id=self.agent_instance_id,
            agent_instance_user_id_list=self.agent_instance_user_id_batch_list,
        )
        for report in existing_report_list:
            existing_report_obj: ExistingReport = existing_report_map.get(report.guid)
            if not existing_report_obj:
                existing_report_map[report.guid] = ExistingReport(
                    idx=report.idx,
                    guid=report.guid,
                    update_hash=report.update_hash,
                    agent_instance_user_details={
                        report.agent_instance_user_id: report.user_bi_report_id
                    },
                )
            else:
                existing_report_obj.agent_instance_user_details[
                    report.agent_instance_user_id
                ] = report.user_bi_report_id
        self.existing_report_map = existing_report_map
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)
        logger.debug(
            f"Existing report aggregate generated successfully for the sync_id {self.sync_id}"
        )
        self.check_running_status()

    def generate_existing_folder_aggregate(self) -> None:
        """This method is used to construct existing folder aggregate"""
        logger.debug(
            f"Starting to generate existing folder aggregate for the sync_id {self.sync_id}"
        )
        existing_folder_map: dict[str, ExistingFolder] = {}
        existing_folder_list: List[BIFolderDetails] = bi_folder.get_folders(
            self.db,
            agent_instance_id=self.agent_instance_id,
            agent_instance_user_id_list=self.agent_instance_user_id_batch_list,
        )
        logger.debug(
            f"Getting existing folders from db for the sync_id {self.sync_id}..."
        )
        for folder in existing_folder_list:
            existing_folder_obj: ExistingFolder = existing_folder_map.get(folder.guid)
            if not existing_folder_obj:

                existing_folder_map[folder.guid] = ExistingFolder(
                    idx=folder.idx,
                    guid=folder.guid,
                    agent_instance_user_details={
                        folder.agent_instance_user_id: FolderUserDetails(
                            folder.user_bi_folder_id, folder.bi_report_count
                        )
                    },
                )
            else:
                existing_folder_obj.agent_instance_user_details[
                    folder.agent_instance_user_id
                ] = FolderUserDetails(folder.user_bi_folder_id, folder.bi_report_count)
        self.existing_folder_map = existing_folder_map
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)
        logger.debug(
            f"Existing folder aggregate generated successfully for the sync_id {self.sync_id}"
        )
        self.check_running_status()

    def add_folder(self, incoming_folder: IncomingFolder) -> None:
        """This method is used to add folder to folders_to_be_inserted list

        Parameters
        ----------
        incoming_folder : IncomingFolder
            Incoming folder data to be inserted
        """
        depth: int = incoming_folder.depth
        if depth not in self.folders_to_be_inserted:
            self.folders_to_be_inserted[depth] = [incoming_folder.guid]
        else:
            self.folders_to_be_inserted[depth].append(incoming_folder.guid)

    def add_folder_user_mapping(
        self,
        incoming_folder: IncomingFolder,
        existing_folder: Optional[ExistingFolder] = None,
    ) -> None:
        """This method is used to find and add new non existing user mappings to the given folder

        Parameters
        ----------
        incoming_folder : IncomingFolder
            Incoming folder data
        existing_folder : Optional[ExistingFolder], optional
            Existing folder data, by default None
        """
        folder_users_to_be_added: list[int] = []
        if existing_folder:
            folder_users_to_be_added = list(
                set(incoming_folder.agent_instance_users)
                - set(existing_folder.agent_instance_user_details)
            )
        else:
            folder_users_to_be_added = incoming_folder.agent_instance_users
        for agent_instance_user_id in folder_users_to_be_added:
            if agent_instance_user_id in self.folder_user_mapping_to_be_inserted:
                self.folder_user_mapping_to_be_inserted[agent_instance_user_id].append(
                    incoming_folder.guid
                )
            else:
                self.folder_user_mapping_to_be_inserted[agent_instance_user_id] = [
                    incoming_folder.guid
                ]

    def add_report_user_mapping(
        self,
        *,
        incoming_report: IncomingReport,
        existing_report: Optional[ExistingReport] = None,
    ) -> None:
        """This method is used to find and add new non existing user mappings to the given report

        Parameters
        ----------
        incoming_report : IncomingReport
            Incoming report data
        existing_report : Optional[ExistingReport], optional
            Existing report data, by default None
        """
        report_users_to_be_added: list[int] = []
        if existing_report:
            report_users_to_be_added = list(
                set(incoming_report.agent_instance_users)
                - set(existing_report.agent_instance_user_details)
            )
        else:
            report_users_to_be_added = incoming_report.agent_instance_users
        for agent_instance_user_id in report_users_to_be_added:
            if agent_instance_user_id in self.report_user_mapping_to_be_inserted:
                self.report_user_mapping_to_be_inserted[agent_instance_user_id].append(
                    incoming_report.guid
                )
            else:
                self.report_user_mapping_to_be_inserted[agent_instance_user_id] = [
                    incoming_report.guid
                ]

    def add_sync_report_log(
        self, agent_instance_user_id: int, bi_report_id: int, report_sync_status: int
    ) -> None:
        """This method is used to add sync report log for the bi_report_id

        Parameters
        ----------
        agent_instance_user_id : int
            agent_instance_user_id of the report and user
        bi_report_id : int
            id of the bi_report
        report_sync_status : int
            status of the report on sync added,granted or revoked (codes.REPORT_SYNC_STATUS)
        """
        # This method adds the new sync_report_log for the first batch of users for whom
        # reports is added/granted/revoked and for the upcoming batches of users
        # This method updates the user_id_list by concatenating with already added batches
        # This approach is followed to save memory consumptions
        sync_report_log_id: Optional[int] = self.report_id_log_id_map.get(bi_report_id)
        user_id: int = self.agent_instance_user_id_map[agent_instance_user_id]
        if not sync_report_log_id:
            # There is no previous log entries for the reports on this sync
            # so new entries is added
            sync_reports_log_obj: Optional[
                dict
            ] = self.sync_reports_log_to_be_inserted.get(bi_report_id)
            if not sync_reports_log_obj:
                self.sync_reports_log_to_be_inserted[bi_report_id] = {
                    "sync_log_id": self.sync_id,
                    "agent_instance_id": self.agent_instance_id,
                    "bi_report_id": bi_report_id,
                    "user_id_list": f"{user_id},",
                    "status": report_sync_status,
                    "created_by": self.user_id,
                    "updated_by": self.user_id,
                }
            else:
                sync_reports_log_obj["user_id_list"] += f"{user_id},"
        else:
            # Log entries for the reports of this sync already exists
            # so user_id_list is updated by concatenating with existing user'id list for the report
            sync_reports_log_update_obj: Optional[
                dict
            ] = self.sync_reports_log_to_be_updated.get(bi_report_id)
            if not sync_reports_log_update_obj:
                self.sync_reports_log_to_be_updated[bi_report_id] = {
                    "idx": sync_report_log_id,
                    "user_id_list": f"{user_id},",
                    "updated_by": self.user_id,
                }
            else:
                sync_reports_log_update_obj["user_id_list"] += f"{user_id},"

    def update_folder_user_report_count(
        self, incoming_folder: IncomingFolder, existing_folder: ExistingFolder
    ) -> None:
        """This method is used to find and update folder user report count changes for the existing folders
           by comparing with incoming folders

        Parameters
        ----------
        incoming_folder : IncomingFolder
            Incoming folder data
        existing_folder : ExistingFolder
            Existing folder data
        """
        # computing folder_report_user_count set(agent_instance_user_id,user_detail.bi_report_count)
        #  for the existing folder
        existing_folder_report_count_set: set = set()
        for (
            agent_instance_user_id,
            user_detail,
        ) in existing_folder.agent_instance_user_details.items():
            existing_folder_report_count_set.add(
                (agent_instance_user_id, user_detail.bi_report_count)
            )
        # set difference of existing_folder_report_count_set and existing_folder_report_count_set
        #  will provide the set of folder report counts to be updated
        folder_report_count_update: set = existing_folder_report_count_set - set(
            incoming_folder.user_report_count_map.items()
        )
        for agent_instance_user_id, existing_report_count in folder_report_count_update:
            updated_report_count: int = incoming_folder.user_report_count_map.get(
                agent_instance_user_id, 0
            )
            if existing_report_count != updated_report_count:
                self.folder_user_report_count_update.append(
                    FolderReportCountUpdate(
                        user_bi_folder_id=existing_folder.agent_instance_user_details[
                            agent_instance_user_id
                        ].user_bi_folder_id,
                        bi_report_count=updated_report_count,
                    )
                )

    def remove_reports(self) -> None:
        """This method is used to remove reports and its user mappings of the
        current agent_instance_user batch which is in existing_report_map and not incoming_report_map
        """
        report_guid_set_to_be_deleted: set[str] = set(self.existing_report_map) - set(
            self.incoming_report_map
        )
        for report in report_guid_set_to_be_deleted:
            existing_report: ExistingReport = self.existing_report_map.get(report)
            # Removing user mappings for existing reports which is not in incoming reports
            self.remove_report_user_mapping(existing_report=existing_report)

            # batch_reports_to_be_deleted is used in admin sync to find stalled reports of the sync
            self.batch_reports_to_be_deleted.add(existing_report.idx)

        self.check_running_status()

    def remove_folders(self) -> None:
        """This method is used to remove folders and its user mappings of the
        current agent_instance_user batch which is in existing_folder_map and not incoming_folder_map
        """
        folder_guid_set_to_be_deleted: set[str] = set(self.existing_folder_map) - set(
            self.incoming_folder_map
        )
        for folder in folder_guid_set_to_be_deleted:
            existing_folder: ExistingFolder = self.existing_folder_map.get(folder)
            # Removing user mappings for existing folders which is not in incoming folders
            self.remove_folder_user_mapping(existing_folder=existing_folder)

            # batch_folders_to_be_deleted is used in admin sync to find stalled folders of the sync
            self.batch_folders_to_be_deleted.add(existing_folder.idx)
        self.check_running_status()

    def remove_user_report_item_mappings(
        self, agent_instance_user_id: int, bi_report_id: int
    ) -> None:
        """This method is used to add user_report_item_guid to user_report_item_guid_to_be_deleted
           for reports which are revoked for the agent_instance_user_id, which will be used to
           delete report references on other tables (user_favorites,user_history,user_report,item_tag)

        Parameters
        ----------
        agent_instance_user_id : int
            agent_instance_user_id of the user
        bi_report_id : int
            id of the bi_report
        """
        user_id: int = self.agent_instance_user_id_map[agent_instance_user_id]
        # computing guid hash with user_id,item_type,bi_report_id fields
        self.user_report_item_guid_to_be_deleted.append(
            sha1(
                "_".join(
                    [
                        str(user_id),
                        str(codes.ITEM_TYPE_MAP["bi_report"]),
                        str(bi_report_id),
                    ]
                ).encode()
            ).hexdigest()
        )
        self.check_running_status()

    def remove_report_user_mapping(
        self,
        existing_report: ExistingReport,
        incoming_report: Optional[IncomingReport] = None,
    ) -> None:
        """This method is used to find report user mapping to be revoked for the users of that report and
            add it to report_user_mapping_to_be_deleted list

        Parameters
        ----------
        existing_report : ExistingReport
            Existing report data
        incoming_report : Optional[IncomingReport], optional
            Incoming report data, by default None
        """
        report_users_to_be_deleted: List[int] = []
        if incoming_report:
            # If the report is in incoming_reports set difference of existing report users and incoming report users
            # will provide users to be revoked for the report
            report_users_to_be_deleted = list(
                set(existing_report.agent_instance_user_details)
                - set(incoming_report.agent_instance_users)
            )
        else:
            # If the report is not in incoming_reports all existing users should be revoked for the report
            report_users_to_be_deleted = existing_report.agent_instance_user_details

        for agent_instance_user_id in report_users_to_be_deleted:
            self.report_user_mapping_to_be_deleted.append(
                existing_report.agent_instance_user_details[agent_instance_user_id]
            )

            self.add_sync_report_log(
                agent_instance_user_id=agent_instance_user_id,
                bi_report_id=existing_report.idx,
                report_sync_status=codes.REPORT_SYNC_STATUS["revoked"],
            )
            # Removing report references of the user in other tables(user_favorites,user_history,user_report,item_tag)

            self.remove_user_report_item_mappings(
                agent_instance_user_id=agent_instance_user_id,
                bi_report_id=existing_report.idx,
            )

    def remove_folder_user_mapping(
        self,
        existing_folder: ExistingFolder,
        incoming_folder: Optional[IncomingFolder] = None,
    ) -> None:
        """This method is used to find folder user mapping to be revoked for the users of that folder and
            add it to folder_user_mapping_to_be_deleted list
        Parameters
        ----------
        existing_folder : ExistingFolder
            Existing folder data
        incoming_folder : Optional[IncomingFolder], optional
            Incoming folder data, by default None
        """
        folder_users_to_be_deleted: List[int] = []
        if incoming_folder:
            # If the folder is in incoming_folders set difference of existing folder users and incoming folder users
            # will provide users to be revoked for the folder
            folder_users_to_be_deleted = list(
                set(existing_folder.agent_instance_user_details)
                - set(incoming_folder.agent_instance_users)
            )
        else:
            # If the folder is not in incoming_folders all existing users should be revoked for the folder
            folder_users_to_be_deleted = existing_folder.agent_instance_user_details
        for agent_instance_user_id in folder_users_to_be_deleted:
            user_bi_folder_id: int = existing_folder.agent_instance_user_details[
                agent_instance_user_id
            ].user_bi_folder_id
            self.folder_user_mapping_to_be_deleted.append(user_bi_folder_id)

    def insert_folders_db(self) -> dict[str, int]:
        """This method is used to insert folders in folders_to_be_inserted list into db

        Returns
        -------
        dict[str,int]
            returns folder_guid_id_map which has id's for inserted folders mapped by guid
        """
        folder_guid_id_map: dict[str, int] = {}
        if self.folders_to_be_inserted:
            logger.debug(f"Inserting folders for the sync_id {self.sync_id}...")

            folder_guid_list: List[str] = []
            created_at: int = codes.DEFAULT_TIME()

            # Folders are checked if it already exists or exists and in deleted state
            # If the folder is in deleted state its status is changed to codes.ENABLED
            for depth in sorted(self.folders_to_be_inserted):
                for folder_guid in self.folders_to_be_inserted[depth]:
                    folder_guid_list.append(folder_guid)

            bi_folder_list: List[BIFolder] = bi_folder.get_folders_by_guid(
                self.db,
                agent_instance_id=self.agent_instance_id,
                folder_guid_list=folder_guid_list,
            )
            logger.debug(
                f"Enabling folders in deleted state for the sync_id {self.sync_id}..."
            )
            enable_deleted_folders: List[dict] = []
            for folder in bi_folder_list:
                folder_guid_id_map[folder.guid] = folder.idx
                if folder.status == codes.DELETED:
                    enable_deleted_folders.append(
                        {"idx": folder.idx, "status": codes.ENABLED}
                    )

            logger.debug(
                f"Enabled deleted folders successfully for the sync_id {self.sync_id}"
            )
            bi_folder.enable_deleted_folders(
                self.db, folder_details=enable_deleted_folders
            )

            # Folders will be inserted in order of increasing depth to maintain adjacency list relation
            for depth in sorted(self.folders_to_be_inserted):
                batch_folders_to_be_inserted: List[dict] = []
                folders_to_be_inserted_guid_set: set[str] = set()
                for folder_guid in self.folders_to_be_inserted[depth]:
                    if folder_guid not in folder_guid_id_map:
                        source_folder_id: Optional[int] = None
                        incoming_folder: IncomingFolder = self.incoming_folder_map[
                            folder_guid
                        ]
                        source_folder_path: str = incoming_folder.path[
                            : -len(f"{incoming_folder.name}{codes.path_delimiter}")
                        ]
                        source_folder_guid: str = sha1(
                            "_".join(
                                [str(self.agent_instance_id), source_folder_path]
                            ).encode()
                        ).hexdigest()

                        if depth != codes.FOLDER_ROOT_LEVEL_DEPTH:
                            existing_source_folder: ExistingFolder = (
                                self.existing_folder_map.get(source_folder_guid)
                            )
                            if existing_source_folder:
                                source_folder_id = existing_source_folder.idx
                            else:
                                source_folder_id = folder_guid_id_map[
                                    source_folder_guid
                                ]
                        batch_folders_to_be_inserted.append(
                            {
                                "name": incoming_folder.name,
                                "source_folder_id": source_folder_id,
                                "path": incoming_folder.path,
                                "agent_instance_id": incoming_folder.agent_instance_id,
                                "depth": incoming_folder.depth,
                                "guid": incoming_folder.guid,
                                "created_at": created_at,
                                "updated_at": created_at,
                                "created_by": self.user_id,
                                "updated_by": self.user_id,
                            }
                        )
                        folders_to_be_inserted_guid_set.add(incoming_folder.guid)

                if batch_folders_to_be_inserted:
                    bi_folder.insert_folders(
                        self.db, folder_list=batch_folders_to_be_inserted
                    )
                    # Fetching inserted folders id's
                    inserted_folders: List[
                        BIFolder
                    ] = bi_folder.get_folders_by_creation_time(
                        self.db,
                        created_at=created_at,
                        depth=depth,
                        agent_instance_id=self.agent_instance_id,
                        created_by=self.user_id,
                    )
                    inserted_folders_guid_set: set[str] = set()
                    for folder in inserted_folders:
                        folder_guid_id_map[folder.guid] = folder.idx
                        inserted_folders_guid_set.add(folder.guid)
                    # Fetching folders which are not inserted by this sync due to integrity error
                    integrity_error_folders_guid: list[str] = list(
                        folders_to_be_inserted_guid_set - inserted_folders_guid_set
                    )
                    if integrity_error_folders_guid:
                        folders = bi_folder.get_folders_by_guid(
                            self.db,
                            agent_instance_id=self.agent_instance_id,
                            folder_guid_list=integrity_error_folders_guid,
                        )
                        for folder in folders:
                            folder_guid_id_map[folder.guid] = folder.idx
                            inserted_folders_guid_set.add(folder.guid)

            logger.debug(
                f"Inserted {len(self.folders_to_be_inserted)} folders successfully for the sync_id {self.sync_id}..."
            )
            self.folders_to_be_inserted.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        return folder_guid_id_map

    def insert_reports_db(self, folder_guid_id_map: dict[str, int]) -> dict[str, int]:
        """This method is used to insert reports in reports_to_be_inserted list into db

        Parameters
        ----------
        folder_guid_id_map : dict[str,int]
            folder_guid_id_map which has id's of inserted folders mapped by its guid's

        Returns
        -------
         dict[str,int]
            report_guid_id_map which has id's of inserted reports mapped by its guid's
        """
        report_guid_id_map: dict[str, int] = {}
        if self.reports_to_be_inserted:
            logger.debug(f"Inserting reports for the sync_id {self.sync_id}...")
            report_data_list: List[dict] = []
            bi_report_list: List[BIReport] = bi_report.get_reports_by_guid_list(
                self.db,
                agent_instance_id=self.agent_instance_id,
                report_guid_list=self.reports_to_be_inserted,
            )
            enable_deleted_reports: List[dict] = []
            created_at: int = codes.DEFAULT_TIME()
            # Reports are checked if it already exists or exists and in deleted state
            # If the report is in deleted state its status is changed to codes.ENABLED
            reports_to_be_inserted_guid_set: set[str] = set()
            for report in bi_report_list:
                report_guid_id_map[report.guid] = report.idx
                if report.status == codes.DELETED:
                    enable_deleted_reports.append(
                        {
                            "idx": report.idx,
                            "status": codes.ENABLED,
                            "updated_at": codes.DEFAULT_TIME(),
                            "updated_by": self.user_id,
                        }
                    )
            logger.debug(
                f"Enabling reports in deleted state for the sync_id {self.sync_id}..."
            )
            bi_report.enable_deleted_reports(
                self.db, report_details=enable_deleted_reports
            )

            for report_guid in self.reports_to_be_inserted:
                if report_guid not in report_guid_id_map:
                    incoming_report: IncomingReport = self.incoming_report_map[
                        report_guid
                    ]
                    source_folder_guid = sha1(
                        "_".join(
                            [str(self.agent_instance_id), incoming_report.path]
                        ).encode()
                    ).hexdigest()
                    existing_folder: ExistingFolder = self.existing_folder_map.get(
                        source_folder_guid
                    )
                    bi_folder_id: int = 0
                    if existing_folder:
                        bi_folder_id = existing_folder.idx
                    else:
                        bi_folder_id = folder_guid_id_map[source_folder_guid]
                    report_data_list.append(
                        {
                            "name": incoming_report.name,
                            "bi_folder_id": bi_folder_id,
                            "path": incoming_report.path,
                            "agent_instance_id": self.agent_instance_id,
                            "url": incoming_report.url,
                            "url_t": incoming_report.url_t,
                            "description": incoming_report.description,
                            "meta": incoming_report.meta,
                            "sync_metadata": incoming_report.sync_metadata,
                            "guid": incoming_report.guid,
                            "update_hash": incoming_report.update_hash,
                            "status": codes.ENABLED,
                            "created_at": created_at,
                            "updated_at": created_at,
                            "created_by": self.user_id,
                            "updated_by": self.user_id,
                        }
                    )
                    reports_to_be_inserted_guid_set.add(incoming_report.guid)
            if report_data_list:
                bi_report.insert_reports(self.db, report_list=report_data_list)
                inserted_reports: List[
                    BIReport
                ] = bi_report.get_reports_by_creation_time(
                    self.db,
                    created_at=created_at,
                    agent_instance_id=self.agent_instance_id,
                    created_by=self.user_id,
                )
                inserted_reports_guid_set: set[str] = set()
                # Fetching inserted report id's
                for report in inserted_reports:
                    report_guid_id_map[report.guid] = report.idx
                    inserted_reports_guid_set.add(report.guid)
                integrity_error_reports_guid: list[str] = list(
                    reports_to_be_inserted_guid_set - inserted_reports_guid_set
                )
                # Fetching reports which are not inserted by this sync due to integrity error
                if integrity_error_reports_guid:
                    reports = bi_report.get_reports_by_guid_list(
                        self.db,
                        agent_instance_id=self.agent_instance_id,
                        report_guid_list=integrity_error_reports_guid,
                    )
                    for report in reports:
                        report_guid_id_map[report.guid] = report.idx
            logger.debug(
                f"Inserted {len(self.reports_to_be_inserted)} reports successfully for the sync_id {self.sync_id}..."
            )
            self.reports_to_be_inserted.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        return report_guid_id_map

    def insert_folder_users_db(self, folder_guid_id_map: dict[str, int]) -> None:
        """This method is used to insert folder user mappings in folder_user_mapping_to_be_inserted list into db

        Parameters
        ----------
        folder_guid_id_map : dict[str,int]
            folder_guid_id_map which has id's of inserted folders mapped by its guid's
        """
        if self.folder_user_mapping_to_be_inserted:
            logger.debug(
                f"Inserting folder user mappings for the sync_id {self.sync_id}..."
            )
            insert_folder_users: List[dict] = []
            for (
                agent_instance_user_id,
                folder_guid_list,
            ) in self.folder_user_mapping_to_be_inserted.items():
                for folder_guid in folder_guid_list:

                    incoming_folder_obj: IncomingFolder = self.incoming_folder_map[
                        folder_guid
                    ]
                    existing_folder_obj: ExistingFolder = self.existing_folder_map.get(
                        folder_guid
                    )
                    folder_id: int = 0
                    if existing_folder_obj:
                        folder_id = existing_folder_obj.idx
                    else:
                        folder_id = folder_guid_id_map[folder_guid]

                    insert_folder_users.append(
                        {
                            "agent_instance_user_id": agent_instance_user_id,
                            "bi_folder_id": folder_id,
                            "bi_report_count": incoming_folder_obj.user_report_count_map[
                                agent_instance_user_id
                            ],
                            "status": codes.ENABLED,
                            "created_by": self.user_id,
                            "updated_by": self.user_id,
                        }
                    )
            if insert_folder_users:
                user_bi_folder.insert_folder_users(
                    self.db, folder_user_list=insert_folder_users
                )
            logger.debug(
                f"Inserted folder user mappings successfully for the sync_id {self.sync_id}..."
            )
            self.folder_user_mapping_to_be_inserted.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        self.check_running_status()

    def insert_report_users_db(self, report_guid_id_map: dict[str, int]) -> None:
        """This method is used to insert report user mappings in report_user_mapping_to_be_inserted list into db

        Parameters
        ----------
        report_guid_id_map : dict[str,int]
            report_guid_id_map which has id's of inserted reports mapped by its guid's
        """
        if self.report_user_mapping_to_be_inserted:
            logger.debug(
                f"Inserting report user mappings for the sync_id {self.sync_id}..."
            )
            insert_report_users: List[dict] = []

            for (
                agent_instance_user_id,
                report_guid_set,
            ) in self.report_user_mapping_to_be_inserted.items():
                for report_guid in report_guid_set:
                    existing_report_obj: ExistingReport = self.existing_report_map.get(
                        report_guid
                    )
                    bi_report_id: int = 0
                    if existing_report_obj:
                        bi_report_id = existing_report_obj.idx

                    else:
                        bi_report_id = report_guid_id_map[report_guid]
                    insert_report_users.append(
                        {
                            "agent_instance_user_id": agent_instance_user_id,
                            "bi_report_id": bi_report_id,
                            "status": codes.ENABLED,
                            "created_by": self.user_id,
                            "updated_by": self.user_id,
                        }
                    )
                    # Adding sync reports log
                    self.add_sync_report_log(
                        agent_instance_user_id=agent_instance_user_id,
                        bi_report_id=bi_report_id,
                        report_sync_status=codes.REPORT_SYNC_STATUS["granted"]
                        if existing_report_obj
                        else codes.REPORT_SYNC_STATUS["added"],
                    )

            if insert_report_users:
                user_bi_report.insert_report_users(
                    self.db, report_user_list=insert_report_users
                )
            logger.debug(
                f"Inserted report user mappings successfully for the sync_id {self.sync_id}..."
            )
            self.report_user_mapping_to_be_inserted.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        self.check_running_status()

    def insert_sync_report_logs_db(self) -> None:
        """This method is used to insert sync_reports_log in sync_reports_log_to_be_inserted list into db"""
        if self.sync_reports_log_to_be_inserted or self.sync_reports_log_to_be_updated:
            logger.debug(
                f"Inserting/Updating sync reports log for the sync_id {self.sync_id}..."
            )
            created_at: int = codes.DEFAULT_TIME()
            if self.sync_reports_log_to_be_inserted:
                insert_sync_reports_log_list = list(
                    self.sync_reports_log_to_be_inserted.values()
                )
                for insert_sync_report in insert_sync_reports_log_list:
                    insert_sync_report["created_at"] = created_at
                    insert_sync_report["updated_at"] = created_at

                sync_reports_log.insert_sync_reports_log(
                    self.db, insert_sync_reports_log_list
                )
                sync_report_log_list: List[
                    SyncReportsLog
                ] = sync_reports_log.get_log_by_creation_time(
                    self.db,
                    created_at=created_at,
                    agent_instance_id=self.agent_instance_id,
                    sync_id=self.sync_id,
                )
                for sync_report_log_obj in sync_report_log_list:
                    self.report_id_log_id_map[
                        sync_report_log_obj.bi_report_id
                    ] = sync_report_log_obj.idx
                logger.debug(
                    f"Inserted {len(self.sync_reports_log_to_be_inserted)} sync reports log for the sync_id {self.sync_id}..."
                )
                self.sync_reports_log_to_be_inserted.clear()
            if self.sync_reports_log_to_be_updated:
                sync_reports_log.update_user_id_list(
                    self.db, list(self.sync_reports_log_to_be_updated.values())
                )
                logger.debug(
                    f"Updated {len(self.sync_reports_log_to_be_updated)} sync reports log for the sync_id {self.sync_id}..."
                )
                self.sync_reports_log_to_be_updated.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        
        self.check_running_status()

    def update_folder_user_report_count_db(self) -> None:
        """Updating folder user's report counts in the folder_user_report_count_update list on db"""
        if self.folder_user_report_count_update:
            logger.debug(
                f"Updating folder user's report counts for the sync_id {self.sync_id}..."
            )
            folder_user_report_count: List[dict] = []
            for folder_report_count_detail in self.folder_user_report_count_update:
                folder_user_report_count.append(
                    {
                        "idx": folder_report_count_detail.user_bi_folder_id,
                        "bi_report_count": folder_report_count_detail.bi_report_count,
                        "updated_by": self.user_id,
                        "updated_at": codes.DEFAULT_TIME(),
                    }
                )
            user_bi_folder.update_folder_users(
                self.db, folder_user_list=folder_user_report_count
            )
            logger.debug(
                f"Updated {len(self.folder_user_report_count_update)} folder user's report counts for the sync_id {self.sync_id}"
            )
            self.folder_user_report_count_update.clear()
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)
        self.check_running_status()

    def update_reports_db(self) -> None:
        """Updating reports in the reports_to_be_updated list on db"""
        if self.reports_to_be_updated:
            logger.debug(f"Updating reports for the sync_id {self.sync_id}...")
            bi_report.update_reports(self.db, report_details=self.reports_to_be_updated)
            logger.debug(f"Updated reports for the sync_id {self.sync_id}")
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)

    def update_agent_instance_report_count_db(self) -> None:
        """This method is used to update agent_instance bi_report_count
        in agent_instance table
        """
        report_count: int = bi_report.get_reports_count(
            self.db, agent_instance_id=self.agent_instance_id
        )
        agent_instance.update_bi_report_count(
            self.db,
            agent_instance_id=self.agent_instance_id,
            bi_report_count=report_count,
            user_id=self.user_id,
        )

    def delete_folders_db(self, folders_to_be_deleted: List[int]) -> None:
        """This method is used to delete folders in the folders_to_be_deleted list from db

        Parameters
        ----------
        folders_to_be_deleted : List[int]
            list of folders to be deleted
        """
        if folders_to_be_deleted:
            logger.debug(f"Deleting folders for the sync_id {self.sync_id}...")
            delete_folder_list: List[dict] = []
            for folder_id in folders_to_be_deleted:
                delete_folder_list.append(
                    {
                        "idx": folder_id,
                        "status": codes.DELETED,
                        "updated_by": self.user_id,
                        "updated_at": codes.DEFAULT_TIME(),
                    }
                )
            bi_folder.delete_folders(
                self.db, folder_list=delete_folder_list
            )
            logger.debug(
                f"Deleted {len(folders_to_be_deleted)} folders for the sync_id {self.sync_id}"
            )
            folders_to_be_deleted.clear()
        self.check_running_status()

    def delete_reports_db(self, reports_to_be_deleted: List[int]) -> None:
        """This method is used to delete reports in the reports_to_be_deleted list from db

        Parameters
        ----------
        reports_to_be_deleted : List[int]
            list of report id's to be deleted
        """
        if reports_to_be_deleted:
            logger.debug(f"Deleting reports for the sync_id {self.sync_id}...")
            delete_report_list: List[dict] = []
            for report_id in reports_to_be_deleted:
                delete_report_list.append(
                    {
                        "idx": report_id,
                        "status": codes.DELETED,
                        "updated_by": self.user_id,
                        "updated_at": codes.DEFAULT_TIME(),
                    }
                )
            bi_report.delete_reports(self.db, report_list=delete_report_list)
            logger.debug(
                f"Deleted {len(reports_to_be_deleted)} reports for the sync_id {self.sync_id}"
            )
            reports_to_be_deleted.clear()
        self.check_running_status()

    def delete_folder_users_db(self) -> None:
        """This method is used to delete folder user mappings in the
        folder_user_mapping_to_be_deleted list from db
        """
        if self.folder_user_mapping_to_be_deleted:
            logger.debug(f"Deleting folder user mapping for the sync_id {self.sync_id}...")
            delete_folder_user_list: List[dict] = []
            for user_bi_folder_id in self.folder_user_mapping_to_be_deleted:
                delete_folder_user_list.append(
                    {
                        "idx": user_bi_folder_id,
                        "bi_report_count": 0,
                        "status": codes.DELETED,
                        "updated_by": self.user_id,
                        "updated_at": codes.DEFAULT_TIME(),
                    }
                )
            user_bi_folder.delete_folder_users(
                self.db, folder_user_list=delete_folder_user_list
            )
            logger.debug(
                f"Deleted {len(self.folder_user_mapping_to_be_deleted)} folder user mapping for the sync_id {self.sync_id}"
            )
            self.folder_user_mapping_to_be_deleted.clear()
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)

    def delete_report_users_db(self) -> None:
        """This method is used to delete report user mappings in the
        report_user_mapping_to_be_deleted list from db
        """
        if self.report_user_mapping_to_be_deleted:
            logger.debug(f"Deleting report user mapping for the sync_id {self.sync_id}...")
            delete_report_user_list: List[dict] = []
            for user_bi_report_id in self.report_user_mapping_to_be_deleted:
                delete_report_user_list.append(
                    {
                        "idx": user_bi_report_id,
                        "status": codes.DELETED,
                        "updated_by": self.user_id,
                        "updated_at": codes.DEFAULT_TIME(),
                    }
                )
            user_bi_report.delete_report_users(
                self.db, report_user_list=delete_report_user_list
            )
            logger.debug(
                f"Deleted {len(self.report_user_mapping_to_be_deleted)} report user mapping for the sync_id {self.sync_id}"
            )
            self.report_user_mapping_to_be_deleted.clear()
        if not self.is_admin_sync:
            self.update_progress(5, is_increment=True)

    def delete_user_report_item_mappings(self) -> None:
        """This method is used to delete user_report_item_mappings in the
        user_report_item_guid_to_be_deleted list from db
        """
        # user_report_item_guid_to_be_deleted list has guid's(user_id,item_type,bi_report_id) to be deleted
        # These guid's are checked for records to be deleted in user_report,user_history,user_favorite,user_report
        if self.user_report_item_guid_to_be_deleted:
            logger.debug(
                f"Deleting user_report_item_mappings for the sync_id {self.sync_id}..."
            )
            start: int = 0
            end: int = len(self.user_report_item_guid_to_be_deleted)
            limit: int = 1000
            while start < end:
                limited_guid_list = self.user_report_item_guid_to_be_deleted[
                    start : start + min(limit, end - start)
                ]
                user_report.delete_user_report_items(
                    self.db,
                    user_report_item_guid_list=limited_guid_list,
                    user_id=self.user_id,
                )
                user_history.delete_user_report_items(
                    self.db,
                    user_report_item_guid_list=limited_guid_list,
                    user_id=self.user_id,
                )
                user_favorite.delete_user_report_items(
                    self.db,
                    user_report_item_guid_list=limited_guid_list,
                    user_id=self.user_id,
                )
                item_tag.delete_user_report_items(
                    self.db,
                    user_report_item_guid_list=limited_guid_list,
                    user_id=self.user_id,
                )
                start += min(limit, end - start)
            logger.debug(
                f"Deleted user_report_item_mappings for the sync_id {self.sync_id}"
            )
            self.user_report_item_guid_to_be_deleted.clear()
        if not self.is_admin_sync:
            self.update_progress(10, is_increment=True)
        self.check_running_status()

    def sync_agent_instance_user_reports(self,start) -> None:
        """This method is used to perform sync for the batch of agent users present in
        agent_instance_user_id_batch_list
        """
        self.generate_incoming_report_folder_aggregate(
            incoming_report_details=get_reports(
                start,
                agent_instance_user_id_list=self.agent_instance_user_id_batch_list,
                bi_report_count=1,
                
            )
        )
        self.generate_existing_report_aggregate()
        self.generate_existing_folder_aggregate()
        
        # Removing existing folders and reports for users that are not present in incoming_report_map
        self.remove_folders()
        self.remove_reports()
        logger.debug("Processing incoming reports...")
        for incoming_report_guid, incoming_report in self.incoming_report_map.items():
            existing_report: ExistingReport = self.existing_report_map.get(
                incoming_report_guid
            )
            if existing_report:
                self.add_report_user_mapping(
                    incoming_report=incoming_report, existing_report=existing_report
                )
                if incoming_report.update_hash != existing_report.update_hash:
                    self.reports_to_be_updated.append(
                        {
                            "idx": existing_report.idx,
                            "name": incoming_report.name,
                            "description": incoming_report.description,
                            "url": incoming_report.url,
                            "url_t": incoming_report.url_t,
                            "meta": incoming_report.meta,
                            "sync_metadata": incoming_report.sync_metadata,
                        }
                    )
                self.remove_report_user_mapping(
                    incoming_report=incoming_report, existing_report=existing_report
                )
                # clearing user information on the report in order to save memory usage
                # existing_report.agent_instance_user_details.clear()
            else:
                # report does not exist
                self.add_report_user_mapping(incoming_report=incoming_report)
                self.reports_to_be_inserted.append(incoming_report_guid)
            # clearing user information on the report in order to save memory usage
            # incoming_report.agent_instance_users.clear()

        logger.debug("Processing incoming folders...")
        for incoming_folder_guid, incoming_folder in self.incoming_folder_map.items():
            existing_folder: ExistingFolder = self.existing_folder_map.get(
                incoming_folder_guid
            )
            if existing_folder:

                self.update_folder_user_report_count(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                self.add_folder_user_mapping(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                self.remove_folder_user_mapping(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                # clearing user information on the folder in order to save memory usage
                # existing_folder.agent_instance_user_details.clear()

            else:
                self.add_folder_user_mapping(incoming_folder=incoming_folder)
                self.add_folder(incoming_folder=incoming_folder)
                # clearing user information on the folder in order to save memory usage
                # incoming_folder.agent_instance_users.clear()
                # incoming_folder.user_report_count_map.clear()

        print("reports:", len(self.reports_to_be_inserted))
        print("folders:", len(self.folders_to_be_inserted))
        print(
            "insert report users:",
            len(self.report_user_mapping_to_be_inserted.get(1, [])),
        )
        print(
            "insert folder users:",
            len(self.folder_user_mapping_to_be_inserted.get(1, [])),
            len(self.folder_user_mapping_to_be_inserted.get(1, [])),
            len(set(self.folder_user_mapping_to_be_inserted.get(1, []))),
        )

        print("delete report users:", len(self.report_user_mapping_to_be_deleted))
        print("delete folder users:", len(self.folder_user_mapping_to_be_deleted))
        print("update folder count users:", len(self.folder_user_report_count_update))
        print("delete reports :", len(self.batch_reports_to_be_deleted))
        print("delete folders :", len(self.batch_folders_to_be_deleted))
        print("user item guid to delete", len(self.user_report_item_guid_to_be_deleted))
        # print("reports:",len(self.reports_to_be_inserted),self.reports_to_be_inserted)
        # print("folders:",len(self.folders_to_be_inserted),self.folders_to_be_inserted)
        # print("insert report users:",len(self.report_user_mapping_to_be_inserted.get(1,[])),self.report_user_mapping_to_be_inserted)
        # print("insert folder users:",len(self.folder_user_mapping_to_be_inserted.get(1,[])),self.folder_user_mapping_to_be_inserted)
        # print("delete report users:",len(self.report_user_mapping_to_be_deleted),len(self.report_user_mapping_to_be_deleted)==len(set(self.report_user_mapping_to_be_deleted)))
        # print("delete folder users:",len(self.folder_user_mapping_to_be_deleted),len(self.folder_user_mapping_to_be_deleted)==len(set(self.folder_user_mapping_to_be_deleted)))
        # print("update folder count users:",len(self.folder_user_report_count_update),self.folder_user_report_count_update)
        # print("user item guid to delete", self.user_report_item_guid_to_be_deleted)

        self.update_reports_db()
        folder_guid_id_map: dict[str, int] = self.insert_folders_db()

        self.insert_folder_users_db(folder_guid_id_map=folder_guid_id_map)
        report_guid_id_map: dict[str, int] = self.insert_reports_db(
            folder_guid_id_map=folder_guid_id_map
        )
        self.insert_report_users_db(report_guid_id_map=report_guid_id_map)

        self.update_folder_user_report_count_db()
        self.delete_folder_users_db()
        self.delete_report_users_db()
        self.delete_user_report_item_mappings()
        self.insert_sync_report_logs_db()
        self.incoming_folder_map.clear()
        self.incoming_report_map.clear()
        self.existing_report_map.clear()
        self.existing_folder_map.clear()

    def sync_agent_instance_user_reports_1(self,start) -> None:
        """This method is used to perform sync for the batch of agent users present in
        agent_instance_user_id_batch_list
        """
        self.generate_incoming_report_folder_aggregate(
            incoming_report_details=get_reports(
                start,
                agent_instance_user_id_list=self.agent_instance_user_id_batch_list,
                bi_report_count=1,
                
            )
        )
        self.generate_existing_report_aggregate()
        self.generate_existing_folder_aggregate()
        
        # Removing existing folders and reports for users that are not present in incoming_report_map
        self.remove_folders()
        self.remove_reports()
        
        logger.debug("Processing incoming folders...")
        index: int = 0
        for incoming_folder_guid, incoming_folder in self.incoming_folder_map.items():
            existing_folder: ExistingFolder = self.existing_folder_map.get(
                incoming_folder_guid
            )
            
            if existing_folder:

                self.update_folder_user_report_count(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                self.add_folder_user_mapping(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                self.remove_folder_user_mapping(
                    incoming_folder=incoming_folder, existing_folder=existing_folder
                )
                # clearing user information on the folder in order to save memory usage
                # existing_folder.agent_instance_user_details.clear()

            else:
                self.add_folder_user_mapping(incoming_folder=incoming_folder)
                self.add_folder(incoming_folder=incoming_folder)
                # clearing user information on the folder in order to save memory usage
                # incoming_folder.agent_instance_users.clear()
                # incoming_folder.user_report_count_map.clear()

            logger.debug("Processing incoming reports...")
            for incoming_report_guid, incoming_report in self.incoming_report_map.items():
                existing_report: ExistingReport = self.existing_report_map.get(
                    incoming_report_guid
                )
                if existing_report:
                    self.add_report_user_mapping(
                        incoming_report=incoming_report, existing_report=existing_report
                    )
                    if incoming_report.update_hash != existing_report.update_hash:
                        self.reports_to_be_updated.append(
                            {
                                "idx": existing_report.idx,
                                "name": incoming_report.name,
                                "description": incoming_report.description,
                                "url": incoming_report.url,
                                "url_t": incoming_report.url_t,
                                "meta": incoming_report.meta,
                                "sync_metadata": incoming_report.sync_metadata,
                            }
                        )
                    self.remove_report_user_mapping(
                        incoming_report=incoming_report, existing_report=existing_report
                    )
                
                else:
                    # report does not exist
                    self.add_report_user_mapping(incoming_report=incoming_report)
                    self.reports_to_be_inserted.append(incoming_report_guid)
            

            folder_guid_id_map: dict[str, int] = self.insert_folders_db()

            self.insert_folder_users_db(folder_guid_id_map=folder_guid_id_map)
            report_guid_id_map: dict[str, int] = self.insert_reports_db(
                folder_guid_id_map=folder_guid_id_map
            )
            self.insert_report_users_db(report_guid_id_map=report_guid_id_map)

            self.update_folder_user_report_count_db()
            self.delete_folder_users_db()
            self.delete_report_users_db()
            self.delete_user_report_item_mappings()
            self.insert_sync_report_logs_db()    

        print("reports:", len(self.reports_to_be_inserted))
        print("folders:", len(self.folders_to_be_inserted))
        print(
            "insert report users:",
            len(self.report_user_mapping_to_be_inserted.get(1, [])),
        )
        print(
            "insert folder users:",
            len(self.folder_user_mapping_to_be_inserted.get(1, [])),
            len(self.folder_user_mapping_to_be_inserted.get(1, [])),
            len(set(self.folder_user_mapping_to_be_inserted.get(1, []))),
        )

        print("delete report users:", len(self.report_user_mapping_to_be_deleted))
        print("delete folder users:", len(self.folder_user_mapping_to_be_deleted))
        print("update folder count users:", len(self.folder_user_report_count_update))
        print("delete reports :", len(self.batch_reports_to_be_deleted))
        print("delete folders :", len(self.batch_folders_to_be_deleted))
        print("user item guid to delete", len(self.user_report_item_guid_to_be_deleted))
        # print("reports:",len(self.reports_to_be_inserted),self.reports_to_be_inserted)
        # print("folders:",len(self.folders_to_be_inserted),self.folders_to_be_inserted)
        # print("insert report users:",len(self.report_user_mapping_to_be_inserted.get(1,[])),self.report_user_mapping_to_be_inserted)
        # print("insert folder users:",len(self.folder_user_mapping_to_be_inserted.get(1,[])),self.folder_user_mapping_to_be_inserted)
        # print("delete report users:",len(self.report_user_mapping_to_be_deleted),len(self.report_user_mapping_to_be_deleted)==len(set(self.report_user_mapping_to_be_deleted)))
        # print("delete folder users:",len(self.folder_user_mapping_to_be_deleted),len(self.folder_user_mapping_to_be_deleted)==len(set(self.folder_user_mapping_to_be_deleted)))
        # print("update folder count users:",len(self.folder_user_report_count_update),self.folder_user_report_count_update)
        # print("user item guid to delete", self.user_report_item_guid_to_be_deleted)

        self.update_reports_db()
        
        self.incoming_folder_map.clear()
        self.incoming_report_map.clear()
        self.existing_report_map.clear()
        self.existing_folder_map.clear()

    def sync_agent_instance_reports(self) -> None:
        """This method is used to perform sync for the agent instance in batches of the agent instance users"""
        # reports_to_be_deleted: set[int] = set()
        # folders_to_be_deleted: set[int] = set()
        self.agent_instance_user_id_map = (
            agent_instance_user.get_agent_instance_user_list(
                self.db, agent_instance_id=self.agent_instance_id
            )
        )
        agent_instance_user_id_list: List[int] = list(
            self.agent_instance_user_id_map.keys()
        )
        agent_instance_user_id_list = agent_instance_user_id_list[:2]
        start: int = 0
        end: int = len(agent_instance_user_id_list)
        # Max limit 1000 to provide oracle support and to control memory usage limit
        # If need to increase limit above 1000 code have to be checked for support and refactored
        # on places where self.agent_instance_user_id_batch_list is used

        max_limit: int = 1000
        while start < end:
            limit: int = min(max_limit, end - start)
            logger.debug(
                f"Started report for users from {start} to {limit} of sync_id {self.sync_id}..."
            )
            self.update_progress(int(start / end * 95))
            slice_range: slice = slice(start, start + limit)
            self.agent_instance_user_id_batch_list = agent_instance_user_id_list[
                slice_range
            ]
            self.sync_agent_instance_user_reports(start)
            # if start == 0:
            #     reports_to_be_deleted = self.batch_reports_to_be_deleted.copy()
            #     folders_to_be_deleted = self.batch_folders_to_be_deleted.copy()
            # else:
            #     if self.batch_reports_to_be_deleted:
            #         reports_to_be_deleted.intersection_update(
            #             self.batch_reports_to_be_deleted
            #         )
            #     if self.batch_folders_to_be_deleted:
            #         folders_to_be_deleted.intersection_update(
            #             self.batch_folders_to_be_deleted
            #         )
            self.batch_reports_to_be_deleted.clear()
            self.batch_folders_to_be_deleted.clear()
            start += limit
        reports_to_be_deleted: List[int] = bi_report.get_all_reports_to_be_deleted(
            self.db,
            agent_instance_id=self.agent_instance_id
        )
        self.delete_reports_db(reports_to_be_deleted=reports_to_be_deleted)
        folders_to_be_deleted: List[int] = bi_folder.get_all_folders_to_be_deleted(
            self.db,
            agent_instance_id=self.agent_instance_id
        )
        self.delete_folders_db(folders_to_be_deleted=folders_to_be_deleted)

        print("delete reports:", len(reports_to_be_deleted))
        print("delete folders:", len(folders_to_be_deleted))

    def start(self, user_detail: Optional[UserDetail] = None) -> None:
        """This method is used to start the sync for a agent_instance

        Parameters
        ----------
        user_detail : Optional[UserDetail], optional
            user_detail of user performing user specific report sync
            will be None for admin report sync, by default None

        Raises
        ------
        HTTP500Exception
            UnExpected Exception
        """
        try:
            logger.debug(f"Started report sync for sync_id {self.sync_id}...")
            self.is_admin_sync = not bool(user_detail)
            sync_log.update_log(
                self.db,
                user_id=self.user_id,
                idx=self.sync_id,
                sync_log_update=SyncLogUpdate(
                    start_time=codes.DEFAULT_TIME(),
                    status=codes.SYNC_STATUS["started"],
                ),
            )
            if not user_detail:
                self.sync_agent_instance_reports()
            else:
                self.agent_instance_user_id_map = {
                    user_detail.agent_instance_user_id: user_detail.user_id
                }
                self.agent_instance_user_id_batch_list = [
                    user_detail.agent_instance_user_id
                ]
                self.sync_agent_instance_user_reports()
                # if self.batch_reports_to_be_deleted:
                #     t1=codes.DEFAULT_TIME()
                #     reports_to_be_deleted: List[int] = bi_report.get_reports_to_be_deleted(
                #         db=self.db,
                #         agent_instance_id=self.agent_instance_id,
                #         report_id_list=list(self.batch_reports_to_be_deleted),
                #     )
                #     print("del rep1",codes.DEFAULT_TIME()-t1)
                #     self.delete_reports_db(reports_to_be_deleted=reports_to_be_deleted)
                #     print("del rep2",codes.DEFAULT_TIME()-t1)
                # if self.batch_folders_to_be_deleted:
                #     t1=codes.DEFAULT_TIME()
                #     folders_to_be_deleted: List[int] = bi_folder.get_folders_to_be_deleted(
                #         db=self.db,
                #         agent_instance_id=self.agent_instance_id,
                #         folder_id_list=list(self.batch_folders_to_be_deleted),
                #     )
                #     print("del fol1",codes.DEFAULT_TIME()-t1)
                #     self.delete_folders_db(folders_to_be_deleted=folders_to_be_deleted)
                #     print("del fol2",codes.DEFAULT_TIME()-t1)
            logger.debug(
                f"Report sync of sync_id {self.sync_id} completed successfully"
            )
            self.update_progress(int(100))
            sync_log.update_log(
                self.db,
                user_id=self.user_id,
                idx=self.sync_id,
                sync_log_update=SyncLogUpdate(
                    end_time=codes.DEFAULT_TIME(),
                    status=codes.SYNC_STATUS["success"],
                ),
            )
            self.finish()
        except StopSyncException as identifier:
            self.stop()
        except Exception as identifier:
            logger.exception(identifier)

    def finish(self) -> None:
        """This method is called before sync is completed to
        end report sync process smoothly
        """
        logger.debug("Ending report sync...")
        self.update_agent_instance_report_count_db()
        self.insert_sync_report_logs_db()
        logger.debug("Report sync ended successfully")

    def stop(self) -> None:
        """This method is called when sync is stopped"""
        logger.debug(f"Stopping report sync of sync_id {self.sync_id}...")
        self.finish()
        sync_log.update_log(
            self.db,
            user_id=self.user_id,
            idx=self.sync_id,
            sync_log_update=SyncLogUpdate(
                end_time=codes.DEFAULT_TIME(),
                status=codes.SYNC_STATUS["failed"],
            ),
        )
        logger.debug(f"Report sync of sync_id {self.sync_id} stopped successfully")

    def update_progress(self, progress: int, is_increment: bool = False) -> None:
        """This method is used to update progress of the sync

        Parameters
        ----------
        progress : int
            new progress of the sync
        is_increment : bool
            if progress should be incremented with existing or not
        """
        if is_increment:
            self.progress += progress
        else:
            self.progress = progress
        sync_log.update_log(
            self.db,
            user_id=self.user_id,
            idx=self.sync_id,
            sync_log_update=SyncLogUpdate(progress=max(100, self.progress)),
        )

    def check_running_status(self) -> None:
        """This method is used to check the running status of the sync"""
        status: int = sync_log.get_sync_status(self.db, idx=self.sync_id)
        if status == codes.SYNC_STATUS["started"]:
            return
        raise StopSyncException(
            message=f"Report Sync of sync id {self.sync_id} is interrupted.."
        )

    