from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
import random
from typing import List, Optional, Tuple, Union
from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session
from app.db.session import SessionLocal,ScopedSession
from sqlalchemy.sql.functions import user
from app.api.api_v2.endpoints.user.report_response import get_reports
from app.schemas.bi_report import AgentReports
from app.schemas.bi_folder import AgentFolders, BIFolderCreate
from app.models.user_bi_folder import UserBIFolder
from app.schemas.report_sync import ExistingFolder, ExistingReport, FolderReportCountUpdate, IncomingFolder, IncomingReport, InsertFolders

from app.crud.crud_bi_folder import bi_folder

from app.api.api_v2.endpoints.user.report_response import get_reports
from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.crud.crud_user_bi_folder import user_bi_folder
from app.crud.crud_user_bi_report import user_bi_report
from app.crud.crud_agent_instance_user import agent_instance_user
from app.conf import codes
import json
from time import time
from app.core.worker import Worker
class SyncReports():
    
    def __init__(self,db: Session) -> None:
        self.agent_instance_id: int = 1
        self.user_id: int =1
        self.agent_instance_user_id: int = 1
        self.is_admin_sync: bool = True
        self.sync_id: int = random.randrange(1,10000000)
        self.db = ScopedSession()

        self.agent_instance_user_id_list: list[int] = []
        self.incoming_report_map: dict[str,IncomingReport] = {}
        self.incoming_folder_map: dict[str, IncomingFolder] = {}
        self.existing_report_map: dict[str, ExistingReport] = {}
        self.existing_folder_map: dict[str, ExistingFolder] = {}
        
        self.reports_to_be_inserted:List[str] = [] # list(report_guid)
        self.reports_to_be_updated:List[int] = [] # list(report_id's)
        self.reports_to_be_deleted:List[int] = [] # list(report_id's)
        self.folders_to_be_deleted:List[int] = [] # list(folder_id's)
        
        self.folders_to_be_inserted:dict[int,List[str]] = {} # depth: list of folder guid
        self.report_user_mapping_to_be_deleted: dict[int,List[int]] = {} # agent_instance_user_id: list(report id's)
        self.folder_user_mapping_to_be_deleted: dict[int,List[int]] = {} # agent_instance_user_id: list(folder id's)
        self.report_user_mapping_to_be_inserted: dict[int,List[str]] = {} # agent_instance_user_id: list(report guid)
        self.folder_user_mapping_to_be_inserted: dict[int,List[int]] = {} # agent_instance_user_id: list(folder guid)
        # self.folder_user_report_count_update: dict[int,dict[int,int]] = {} # folder_id: agent_instance_id:new report count
        self.folder_user_report_count_update: List[FolderReportCountUpdate] = [] # folder_id: agent_instance_id:new report count

        
    def generate_incoming_report_folder_aggregate(self,*, incoming_report_details: List[Tuple[int,dict]]) -> None:
        print("0")
        t1=time()
        incoming_report_map: dict[str,IncomingReport] = {}
        incoming_folder_map: dict[str,IncomingFolder] = {}
        for agent_instance_user_id,incoming_reports in incoming_report_details:
            for incoming_report in incoming_reports:
                incoming_report_guid: str = sha1( "_".join([incoming_report['report_id'], str(self.agent_instance_id) , incoming_report['path'] ]).encode()).hexdigest()
                incoming_report_obj: IncomingReport = incoming_report_map.get(incoming_report_guid)
                if  incoming_report_obj :
                    incoming_report_obj.agent_instance_users.append(agent_instance_user_id)
                else:
                    meta: str = json.dumps(incoming_report["meta"])
                    sync_meta: str = json.dumps(incoming_report["sync_metadata"])
                    update_hash: str = sha1("_".join([ incoming_report["name"], incoming_report["description"], incoming_report["url"],meta 
                    ,sync_meta]).encode()).hexdigest()
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
                            source_folder_guid = sha1( "_".join([str(self.agent_instance_id), incoming_report["path"]]).encode()).hexdigest() ,
                            update_hash = update_hash
                        )
                    
                report_folder_path_list: str = incoming_report["path"].rstrip(codes.path_delimiter).split(codes.path_delimiter)
                for index, folder_name in enumerate(report_folder_path_list[::-1]):
                    
                    depth: int = len(report_folder_path_list) - index
                    path: str = codes.path_delimiter.join(report_folder_path_list[:depth]) + codes.path_delimiter
                    guid: str = sha1( "_".join([str(self.agent_instance_id), path ]).encode()).hexdigest()
                    folder: IncomingFolder = incoming_folder_map.get(guid)
                    if not folder:
                        source_folder_path: str = path[:-len(f'{folder_name}{codes.path_delimiter}')]
                        source_folder_guid: str = sha1( "_".join([str(self.agent_instance_id), source_folder_path ]).encode()).hexdigest() 
                        user_report_count: int = 1 if index==0 else 0
                        incoming_folder_map[guid] = IncomingFolder(    
                            name=folder_name, 
                            path=path,
                            agent_instance_id=self.agent_instance_id,
                            depth=depth,
                            guid = guid,
                            agent_instance_users=[agent_instance_user_id],
                            user_report_count_map= {agent_instance_user_id: user_report_count},
                            source_folder_guid=source_folder_guid

                        )
                    else:
                        folder.agent_instance_users.append(agent_instance_user_id) 
                        if index == 0:
                            folder.user_report_count_map[agent_instance_user_id] = folder.user_report_count_map.get(agent_instance_user_id,0)+1 
                        else:
                            folder.user_report_count_map[agent_instance_user_id] = 0        
        
        self.incoming_report_map = incoming_report_map
        self.incoming_folder_map = incoming_folder_map
        t2=time()
        print("report,folder aggregate",t2-t1)
    def generate_existing_report_aggregate(self) -> None:
        print("*1")
        t1=time()
        db: Session = self.db
        existing_report_map: dict[str, ExistingReport] = {}
        if self.is_admin_sync:
            existing_report_list: List[AgentReports] = bi_report.get_reports_by_agent_id(db,agent_instance_id=self.agent_instance_id)
        else:
            existing_report_list: List[AgentReports] = bi_report.get_reports_by_agent_instance_user_id(db,agent_instance_user_id=self.agent_instance_user_id)
        # report_user_mapping_list: List[UserBIReport] = user_bi_report.get_bi_report_user_mapping(db,agent_instance_user_id_list=self.agent_instance_user_id_list)    
        
        #     report_hash: str = report.reportid_agentid_path_hash
        #     existing_report_obj: ExistingReport = existing_report_map.get(report_hash)
        #     if existing_report_obj:
        #         existing_report_obj.agent_users.add(report.agent_user_id)
        #     else:
        #         existing_report_map[report.reportid_agentid_path_hash]= ExistingReport(

        
        for report in existing_report_list:
            existing_report_obj: ExistingReport = existing_report_map.get(report.guid)
            if not existing_report_obj:
                existing_report_map[report.guid]= ExistingReport(
                    idx = report.idx,
                    path= report.path,
                    guid = report.guid,
                    update_hash = report.update_hash,
                    agent_instance_users = [report.agent_instance_user_id]

                )
            else:
                existing_report_obj.agent_instance_users.append(report.agent_instance_user_id)
       
        # report_user_map:dict = {}
        # for report_user in report_user_mapping_list:
        #     if report_user.bi_report_id not in report_user_map:
        #         report_user_map[report_user.bi_report_id] = set([report_user.agent_instance_user_id])
        #     else:
        #         report_user_map[report_user.bi_report_id].add(report_user.agent_instance_user_id)
       
        # for report in existing_report_list:
            
        #     existing_report_map[report.guid]= ExistingReport(
        #             idx = report.idx,
        #             path= report.path,
        #             guid = report.guid,
        #             update_hash = report.update_hash,
        #             agent_instance_users = report_user_map[report.idx]

        #         )
        
        self.existing_report_map = existing_report_map
        t2=time()
        print("report time",t2-t1)
        

    def generate_existing_folder_aggregate(self) -> None:
        print("*2")
        t1= time()
        
        existing_folder_map: dict[str, ExistingFolder] = {}
        if self.is_admin_sync:
            existing_folder_list: List[AgentFolders] = bi_folder.get_folders_by_agent_id(self.db,agent_instance_id=self.agent_instance_id)    
        else:
            existing_folder_list: List[AgentFolders] = bi_folder.get_folders_by_agent_instance_user_id(self.db,agent_instance_user_id=self.agent_instance_user_id) 

        print("*2-1")
        
        for folder in existing_folder_list:
            existing_folder_obj: ExistingFolder = existing_folder_map.get(folder.guid)
            if not existing_folder_obj:
                
                existing_folder_map[folder.guid] = ExistingFolder(
                        idx = folder.idx,
                        guid = folder.guid,
                        agent_instance_users=[folder.agent_instance_user_id],
                        user_report_count_map= {folder.agent_instance_user_id:folder.bi_report_count}

                    )
            else:
                existing_folder_obj.agent_instance_users.append(folder.agent_instance_user_id)
                existing_folder_obj.user_report_count_map[folder.agent_instance_user_id] = folder.bi_report_count
            
        
        # user_folder_mapping_list: List[UserBIFolder] = user_bi_folder.get_bi_folder_user_mapping(self.db,agent_instance_user_id_list=self.agent_instance_user_id_list)
        # user_folder_map: dict = {}
        
        # for user_folder_mapping in user_folder_mapping_list:
        #     if user_folder_mapping.bi_folder_id not in user_folder_map:

        #         user_folder_map[user_folder_mapping.bi_folder_id] = {user_folder_mapping.agent_instance_user_id:user_folder_mapping.bi_report_count}
        #     else:
        #         user_folder_map[user_folder_mapping.bi_folder_id][user_folder_mapping.agent_instance_user_id] = user_folder_mapping.bi_report_count

        # for folder in existing_folder_list:
        #     folder_guid: str = folder.guid
            
        #     existing_folder_obj: ExistingFolder =  ExistingFolder(
        #             idx = folder.idx,
        #             guid = folder_guid,
        #             agent_instance_users=set(user_folder_map.get(folder.idx,{}).keys()),
        #             user_report_count_map= user_folder_map.get(folder.idx,{})

        #         )
        #     existing_folder_map[folder_guid] = existing_folder_obj
            
            
        self.existing_folder_map = existing_folder_map
        t2=time()
        print("folder time",t2-t1, len(existing_folder_list))
        
    def add_folder_user_mapping(self,incoming_folder: IncomingFolder,existing_folder: Optional[ExistingFolder]=None):
        if existing_folder:
            folder_users_to_be_added: list[int] = list(set(incoming_folder.agent_instance_users) - set(existing_folder.agent_instance_users))
        else:
            folder_users_to_be_added: list[int] = incoming_folder.agent_instance_users
        
        for agent_instance_user_id in folder_users_to_be_added:
            if agent_instance_user_id in self.folder_user_mapping_to_be_inserted:
                self.folder_user_mapping_to_be_inserted[agent_instance_user_id].append(incoming_folder.guid)
            else:
                self.folder_user_mapping_to_be_inserted[agent_instance_user_id] = [incoming_folder.guid]
    
    def add_report_user_mapping(self,*, incoming_report: IncomingReport, existing_report: Optional[ExistingReport]=None):
        if existing_report:
            report_users_to_be_added: list[int] = list(set(incoming_report.agent_instance_users) - set(existing_report.agent_instance_users))
        else:
            report_users_to_be_added: list[int] = incoming_report.agent_instance_users
        for agent_instance_user_id in report_users_to_be_added:
            if agent_instance_user_id in self.report_user_mapping_to_be_inserted:
                self.report_user_mapping_to_be_inserted[agent_instance_user_id].append(incoming_report.guid)
            else:
                self.report_user_mapping_to_be_inserted[agent_instance_user_id] = [incoming_report.guid]
    
    def remove_report_user_mapping(self,  existing_report: ExistingReport, incoming_report: Optional[IncomingReport] =None):
        if incoming_report:
            report_users_to_be_deleted: List[int] = list(set(existing_report.agent_instance_users) - set(incoming_report.agent_instance_users))
        else:
            report_users_to_be_deleted: List[int] = existing_report.agent_instance_users
        for agent_instance_user_id in report_users_to_be_deleted:
            if agent_instance_user_id in self.report_user_mapping_to_be_deleted:
                self.report_user_mapping_to_be_deleted[agent_instance_user_id].append(existing_report.idx)
            else:
                self.report_user_mapping_to_be_deleted[agent_instance_user_id] = [existing_report.idx]
    
        # if self.is_admin_sync and len(report_users_to_be_deleted)==len(existing_report.agent_instance_users):
        #     self.reports_to_be_deleted.append(existing_report.idx)

    def remove_folder_user_mapping(self, existing_folder: ExistingFolder, incoming_folder: Optional[IncomingFolder] = None):
        if incoming_folder:
            folder_users_to_be_deleted: List[int] = list(set(existing_folder.agent_instance_users) - set(incoming_folder.agent_instance_users))
        else:
            folder_users_to_be_deleted: List[int] = existing_folder.agent_instance_users
        for agent_instance_user_id in folder_users_to_be_deleted:
            if agent_instance_user_id in self.folder_user_mapping_to_be_deleted:
                self.folder_user_mapping_to_be_deleted[agent_instance_user_id].append(existing_folder.idx)
            else:
                self.folder_user_mapping_to_be_deleted[agent_instance_user_id] = [existing_folder.idx]

        # if self.is_admin_sync and len(folder_users_to_be_deleted)==len(existing_folder.agent_instance_users):
        #     self.folders_to_be_deleted.append(existing_folder.idx)

    def add_folder(self, incoming_folder: IncomingFolder) :
        depth: int = incoming_folder.depth
        if depth not in self.folders_to_be_inserted:
            self.folders_to_be_inserted[depth] = [incoming_folder.guid]
        else:
            self.folders_to_be_inserted[depth].append(incoming_folder.guid)
          
    
    # To do
    # Insert folders
    # Insert reports
    # Insert user report
    # Insert user folders
    # update folders
    # update reports
    # update user report
    # update user folder report
    
    def insert_folders(self) -> dict[str,int]:
        folder_guid_id_map: dict[str,int] = {}
        for depth in sorted(self.folders_to_be_inserted):
            folder_list: List[dict] = []
            for folder_guid in self.folders_to_be_inserted[depth]:
                source_folder_id: Optional[int] = None
                folder_obj: IncomingFolder =self.incoming_folder_map[folder_guid]
                if depth!=codes.FOLDER_ROOT_LEVEL_DEPTH:
                    existing_source_folder: ExistingFolder = self.existing_folder_map.get(folder_obj.source_folder_guid)
                    if existing_source_folder:
                        source_folder_id = existing_source_folder.idx
                    else:
                        source_folder_id = folder_guid_id_map[folder_obj.source_folder_guid]
                folder_list.append({"name":folder_obj.name,"source_folder_id":source_folder_id,"path":folder_obj.path,"agent_instance_id":folder_obj.agent_instance_id,"depth":folder_obj.depth,
                "guid":folder_obj.guid,"sync_id":self.sync_id,"created_by":self.user_id,"updated_by":self.user_id})   
                
            if folder_list:    
                self.db = bi_folder.create_folders(self.db,folder_list=folder_list)
                inserted_folders = bi_folder.get_folders_by_sync_id(self.db,sync_id=self.sync_id, depth=depth)
                for folder in inserted_folders:
                    folder_guid_id_map[folder.guid] = folder.idx
                
                
        return folder_guid_id_map

    def insert_reports(self, folder_guid_id_map: dict[str,int]):
        report_list = []
        report_guid_id_map: dict[str,int] = {}
        
        for report_guid in self.reports_to_be_inserted:
            report_obj =self.incoming_report_map[report_guid]

            existing_folder: ExistingFolder = self.existing_folder_map.get(report_obj.source_folder_guid)
            if existing_folder:
                bi_folder_id: int = existing_folder.idx
            else:
                bi_folder_id: int = folder_guid_id_map[report_obj.source_folder_guid]
            report_list.append(
                {
                    "name": report_obj.name,
                    "bi_folder_id": bi_folder_id,
                    "path": report_obj.path,
                    "agent_instance_id": self.agent_instance_id,
                    "url": report_obj.url,
                    # "url_t": report_obj.url_t,
                    "description": report_obj.description,
                    "guid": report_obj.guid,
                    "update_hash": report_obj.update_hash,
                    "sync_id": self.sync_id,
                    "status": codes.ENABLED,
                    "created_by": self.user_id,
                    "updated_by": self.user_id,
                }
            )
        if report_list:
            self.db = bi_report.create_reports(self.db,report_list=report_list)    
            
            inserted_reports: List[BIReport] = bi_report.get_reports_by_sync_id(self.db,sync_id=self.sync_id)
            for report in inserted_reports:
                report_guid_id_map[report.guid] = report.idx
        return report_guid_id_map

    def insert_folder_users(self, folder_guid_id_map: dict[str,int] ):        
        insert_folder_users = []
        for agent_instance_user_id,folder_guid_set in self.folder_user_mapping_to_be_inserted.items():
            for folder_guid in folder_guid_set:
                
                incoming_folder_obj: IncomingFolder = self.incoming_folder_map[folder_guid]
                existing_folder_obj: ExistingFolder = self.existing_folder_map.get(folder_guid)
                if existing_folder_obj:
                    folder_id: int = existing_folder_obj.idx
                else:
                    folder_id: int = folder_guid_id_map[folder_guid]

                insert_folder_users.append(
                    {
                        "agent_instance_user_id": agent_instance_user_id,
                        "bi_folder_id": folder_id,
                        "bi_report_count": incoming_folder_obj.user_report_count_map[agent_instance_user_id],
                        "status": codes.ENABLED,
                        "created_by": self.user_id,
                        "updated_by": self.user_id
                    }
                )
        if insert_folder_users:
            self.db = user_bi_folder.insert_folder_users(self.db,folder_user_list=insert_folder_users)

    def insert_report_users(self, report_guid_id_map: dict[str,int] ):        
        insert_report_users = []
        for agent_instance_user_id,report_guid_set in self.report_user_mapping_to_be_inserted.items():
            for report_guid in report_guid_set:      
                existing_report_obj: ExistingReport = self.existing_report_map.get(report_guid)
                if existing_report_obj:
                    bi_report_id: int = existing_report_obj.idx
                else:
                    bi_report_id: int = report_guid_id_map[report_guid]
                insert_report_users.append(
                    {
                        "agent_instance_user_id": agent_instance_user_id,
                        "bi_report_id": bi_report_id,
                        "status": codes.ENABLED,
                        "created_by": self.user_id,
                        "updated_by": self.user_id
                    }
                )
        if insert_report_users:
            self.db = user_bi_report.insert_report_users(self.db,report_user_list=insert_report_users)

    def remove_reports(self):
        report_guid_set_to_be_deleted: set[str]  = set(self.existing_report_map) - set(self.incoming_report_map)
        for report in report_guid_set_to_be_deleted:
            existing_report: ExistingReport = self.existing_report_map.get(report)
            self.remove_report_user_mapping(existing_report=existing_report)
            if self.is_admin_sync:
                self.reports_to_be_deleted.append(existing_report.idx)

    
    def remove_folders(self):
        folder_guid_set_to_be_deleted: set[str]  = set(self.existing_folder_map) - set(self.incoming_folder_map)
        for folder in folder_guid_set_to_be_deleted:
            existing_folder: ExistingFolder = self.existing_folder_map.get(folder)
            self.remove_folder_user_mapping(existing_folder=existing_folder)
            if self.is_admin_sync:
                self.folders_to_be_deleted.append(existing_folder.idx)

    def delete_folder_user_mapping(self):
        delete_folder_user_list = []
        for folder_id in self.folders_to_be_deleted:
            delete_folder_user_list.append(
                {
                    "idx": folder_id,
                    "status": codes.DELETED
                }
            )
        self.db = bi_folder.delete_folders(self.db,folder_list=delete_folder_user_list)    
    def delete_folders(self):
        delete_folder_list = []
        for folder_id in self.folders_to_be_deleted:
            delete_folder_list.append(
                {
                    "idx": folder_id,
                    "status": codes.DELETED
                }
            )
        self.db = bi_folder.delete_folders(self.db,folder_list=delete_folder_list)

    def delete_reports(self):
        delete_report_list = []
        for report_id in self.reports_to_be_deleted:
            delete_report_list.append(
                {
                    "idx": report_id,
                    "status": codes.DELETED
                }
            )
        self.db = bi_report.delete_reports(self.db,folder_list=delete_report_list)

    def sync_agent_reports(self): 
        
        self.agent_instance_user_id_list = agent_instance_user.get_agent_instance_user_list(self.db, agent_instance_id =self.agent_instance_id)
        print(len(self.agent_instance_user_id_list))
        self.generate_incoming_report_folder_aggregate(incoming_report_details=get_reports(agent_instance_user_id_list=self.agent_instance_user_id_list,bi_report_count=10)) 
      
        
        # worker: Worker = Worker(worker_count=2)
        # worker.add_job(self.generate_existing_report_aggregate)
        # worker.add_job(self.generate_existing_folder_aggregate)
        # worker.start()
        self.generate_existing_report_aggregate()
        self.generate_existing_folder_aggregate()
        
        for incoming_report_guid,incoming_report in self.incoming_report_map.items():           
            existing_report: ExistingReport = self.existing_report_map.get(incoming_report_guid)
            
            if existing_report:
                self.add_report_user_mapping(incoming_report=incoming_report,existing_report=existing_report)
                if incoming_report.update_hash != existing_report.update_hash:
                    self.reports_to_be_updated.append(existing_report.idx)
                self.remove_report_user_mapping(incoming_report=incoming_report,existing_report=existing_report)
            else:
                # report does not exist
                # self.add_incoming_report_user(incoming_report=incoming_report)
                self.add_report_user_mapping(incoming_report=incoming_report)
                self.reports_to_be_inserted.append(incoming_report_guid)
            
        for incoming_folder_guid,incoming_folder in self.incoming_folder_map.items():
            existing_folder: ExistingFolder = self.existing_folder_map.get(incoming_folder_guid)
            if existing_folder:
                # self.add_existing_folder_user(incoming_folder=incoming_folder,existing_folder=existing_folder)
                folder_report_count_update = set(existing_folder.user_report_count_map.items()) - set(incoming_folder.user_report_count_map.items())
                for agent_instance_user_id,existing_report_count in folder_report_count_update:
                    updated_report_count: int = incoming_folder.user_report_count_map.get(agent_instance_user_id,0)
                    self.folder_user_report_count_update.append(
                        FolderReportCountUpdate(
                            agent_instance_user_id = agent_instance_user_id,
                            bi_folder_id = existing_folder.idx,
                            bi_report_count = updated_report_count
                        )
                    )
                  
                self.add_folder_user_mapping(incoming_folder=incoming_folder,existing_folder=existing_folder)
                self.remove_folder_user_mapping(incoming_folder=incoming_folder,existing_folder=existing_folder)
                pass
            else:
                # self.add_incoming_folder_user(incoming_folder=incoming_folder)
                self.add_folder_user_mapping(incoming_folder=incoming_folder)
                self.add_folder(incoming_folder=incoming_folder)
        
        
        self.remove_folders()
        self.remove_reports()
        

        
        # folder_guid_id_map: dict[str,int] = self.insert_folders()
        # self.insert_folder_users(folder_guid_id_map = folder_guid_id_map)
        # report_guid_id_map: dict[str,int] = self.insert_reports(folder_guid_id_map=folder_guid_id_map)
        # self.insert_report_users(report_guid_id_map = report_guid_id_map)
        
        
        print("reports:",len(self.reports_to_be_inserted))
        print("folders:",len(self.folders_to_be_inserted))
        print("delete reports:",len(self.reports_to_be_deleted))
        print("delete folders:",len(self.folders_to_be_deleted))
        print("report users:",len(self.report_user_mapping_to_be_inserted.get(1,[])))
        print("folder users:",len(self.folder_user_mapping_to_be_inserted.get(1,[])))
        print("insert folder users:",len(self.folder_user_mapping_to_be_inserted))
        
        print("delete folder users:",len(self.folder_user_mapping_to_be_deleted))