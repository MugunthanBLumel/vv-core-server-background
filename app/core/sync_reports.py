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
from app.schemas.report_sync import ExistingFolder, ExistingReport, IncomingFolder, IncomingReport, InsertFolders

from app.crud.crud_bi_folder import bi_folder

from app.api.api_v2.endpoints.user.report_response import get_reports
from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.crud.crud_user_bi_folder import user_bi_folder
from app.crud.crud_user_bi_report import user_bi_report
from app.crud.crud_agent_user import agent_user
from app.conf import codes
import json
from time import time
from app.core.worker import Worker
class SyncReports():
    
    def __init__(self,db: Session) -> None:
        self.agent_id: int = 1
        self.user_id: int =1
        self.agent_user_id: int = 1
        self.is_admin_sync: bool = True
        self.sync_id: int = random.randrange(1,10000000)
        self.db = ScopedSession()

        self.agent_user_id_list: List[int] = []
        self.incoming_report_map: dict[str,IncomingReport] = {}
        self.incoming_folder_map: dict[str, IncomingFolder] = {}
        self.existing_report_map: dict[str, ExistingReport] = {}
        self.existing_folder_map: dict[str, ExistingFolder] = {}
        
        self.reports_to_be_inserted:set[str] = set() # set(report_hash)
        self.reports_to_be_updated:set[int] = set() # set(report_id's)
        self.folders_to_be_inserted:dict[int,set[str]] = {} # depth: set of folder hash
        self.reports_to_be_deleted:set[int] = set() # set(report_id's)
        self.folders_to_be_deleted:set[int] = set() # set(folder_id's)
        self.report_user_mapping_to_be_inserted: dict[int,set[str]] = {} # agent_user_id: set(report hash)
        self.folder_user_mapping_to_be_inserted: dict[int,set[str]] = {} # agent_user_id: set(folder hash)
        self.report_user_mapping_to_be_deleted: dict[int,set[int]] = {} # agent_user_id: set(report id's)
        self.folder_user_mapping_to_be_deleted: dict[int,set[int]] = {} # agent_user_id: set(folder id's)
        self.folder_user_report_count_update: dict[int,dict[int,int]] = {} # folder_id: agent_id:new report count


        self.existing_report_user_to_be_inserted: dict[int,set[int]] = {} # agent_user_id: set(report id's)
        self.incoming_report_user_to_be_inserted: dict[int,set[str]] = {} # agent_user_id: set(report hash)
        
        self.existing_folder_user_to_be_inserted: dict[int,set[int]] = {} # agent_user_id: set(folder id's)
        self.incoming_folder_user_to_be_inserted: dict[int,set[str]] = {} # agent_user_id: set(folder hash)
        
        
        
    def generate_incoming_report_folder_aggregate(self,*, incoming_report_details: List[Tuple[int,dict]]) -> None:
        
        incoming_report_map: dict[str,IncomingReport] = {}
        incoming_folder_map: dict[str,IncomingFolder] = {}
        for agent_user_id,incoming_reports in incoming_report_details:
            for incoming_report in incoming_reports:
                incoming_report_hash: str = sha1( "_".join([incoming_report['report_id'], str(self.agent_id) , incoming_report['path'] ]).encode()).hexdigest()
                incoming_report_obj: IncomingReport = incoming_report_map.get(incoming_report_hash)
                if  incoming_report_obj :
                    incoming_report_obj.agent_users.add(agent_user_id)
                else:
                    meta: str = json.dumps(incoming_report["meta"])
                    sync_meta: str = json.dumps(incoming_report["sync_metadata"])
                    update_hash: str = sha1("_".join([ incoming_report["name"], incoming_report["description"], incoming_report["url"],meta 
                    ,sync_meta]).encode()).hexdigest()
                    incoming_report_map[incoming_report_hash] = IncomingReport(
                            name=incoming_report["name"],
                            description=incoming_report["description"],
                            report_id=incoming_report["report_id"],
                            url=incoming_report["url"],
                            url_t=incoming_report["url_t"],
                            path=incoming_report["path"],
                            meta=meta,
                            sync_metadata=sync_meta,
                            agent_users=set([agent_user_id]),
                            reportid_agentid_path_hash=incoming_report_hash,
                            source_folder_hash = sha1( "_".join([str(self.agent_id), incoming_report["path"]]).encode()).hexdigest() ,
                            update_hash = update_hash
                        )
                    
                report_folder_path_list: str = incoming_report["path"].rstrip(codes.path_delimiter).split(codes.path_delimiter)
                for index, folder_name in enumerate(report_folder_path_list[::-1]):
                    
                    depth: int = len(report_folder_path_list) - index
                    path: str = codes.path_delimiter.join(report_folder_path_list[:depth]) + codes.path_delimiter
                    agent_id_path_hash: str = sha1( "_".join([str(self.agent_id), path ]).encode()).hexdigest()
                    folder: IncomingFolder = incoming_folder_map.get(agent_id_path_hash)
                    if not folder:
                        source_folder_path: str = path[:-len(f'{folder_name}{codes.path_delimiter}')]
                        source_folder_hash: str = sha1( "_".join([str(self.agent_id), source_folder_path ]).encode()).hexdigest() 
                        user_report_count: int = 1 if index==0 else 0
                        incoming_folder_map[agent_id_path_hash] = IncomingFolder(    
                            name=folder_name, 
                            path=path,
                            agent_id=self.agent_id,
                            depth=depth,
                            agent_id_path_hash = agent_id_path_hash,
                            agent_users=set([agent_user_id]),
                            user_report_count_map= {agent_user_id: user_report_count},
                            source_folder_hash=source_folder_hash

                        )
                    else:
                        folder.agent_users.add(agent_user_id) 
                        if index == 0:
                            folder.user_report_count_map[agent_user_id] = folder.user_report_count_map.get(agent_user_id,0)+1 
        
        self.incoming_report_map = incoming_report_map
        self.incoming_folder_map = incoming_folder_map

    def generate_existing_report_aggregate(self) -> None:
        print("*1")
        t1=time()
        db: Session = self.db
        existing_report_map: dict[str, ExistingReport] = {}
        if self.is_admin_sync:
            existing_report_list: List[AgentReports] = bi_report.get_reports_by_agent_id(db,agent_id=self.agent_id)
        else:
            existing_report_list: List[AgentReports] = bi_report.get_reports_by_agent_user_id(db,agent_user_id=self.agent_user_id)
        report_user_mapping_list: List[UserBIReport] = user_bi_report.get_bi_report_user_mapping(db,agent_user_id_list=self.agent_user_id_list)    
        
        report_user_map:dict = {}
        for report_user in report_user_mapping_list:
            if report_user.report_id not in report_user_map:
                report_user_map[report_user.report_id] = set([report_user.agent_user_id])
            else:
                report_user_map[report_user.report_id].add(report_user.agent_user_id)
       
        for report in existing_report_list:
            existing_report_map[report.reportid_agentid_path_hash]= ExistingReport(
                    idx = report.idx,
                    path= report.path,
                    reportid_agentid_path_hash = report.reportid_agentid_path_hash,
                    update_hash = report.update_hash,
                    agent_users = report_user_map[report.idx]

                )
        
        # for report in existing_report_list:
        #     report_hash: str = report.reportid_agentid_path_hash
        #     existing_report_obj: ExistingReport = existing_report_map.get(report_hash)
        #     if existing_report_obj:
        #         existing_report_obj.agent_users.add(report.agent_user_id)
        #     else:
        #         existing_report_map[report.reportid_agentid_path_hash]= ExistingReport(
        #             idx = report.idx,
        #             path= report.path,
        #             reportid_agentid_path_hash = report_hash,
        #             update_hash = report.update_hash,
        #             agent_users=set([report.agent_user_id])

        #         )
        self.existing_report_map = existing_report_map
        t2=time()
        print("report time",t2-t1)
        

    def generate_existing_folder_aggregate(self) -> None:
        print("*2")
        t1= time()
        db: Session = self.db
        existing_folder_map: dict[str, ExistingFolder] = {}
        if self.is_admin_sync:
            existing_folder_list: List[AgentFolders] = bi_folder.get_folders_by_agent_id(db,agent_id=self.agent_id)    
        else:
            existing_folder_list: List[AgentFolders] = bi_folder.get_folders_by_agent_user_id(db,agent_user_id=self.agent_user_id) 


        user_folder_mapping_list: List[UserBIFolder] = user_bi_folder.get_bi_folder_user_mapping(db,agent_user_id_list=self.agent_user_id_list)
        user_folder_map: dict = {}
        
        for user_folder_mapping in user_folder_mapping_list:
            if user_folder_mapping.bi_folder_id not in user_folder_map:

                user_folder_map[user_folder_mapping.bi_folder_id] = {user_folder_mapping.agent_user_id:user_folder_mapping.report_count}
            else:
                user_folder_map[user_folder_mapping.bi_folder_id][user_folder_mapping.agent_user_id] = user_folder_mapping.report_count

        for folder in existing_folder_list:
            folder_hash: str = folder.agent_id_path_hash
            
            existing_folder_obj: ExistingFolder =  ExistingFolder(
                    idx = folder.idx,
                    agent_id_path_hash = folder_hash,
                    agent_users=set(user_folder_map.get(folder.idx,{}).keys()),
                    user_report_count_map= user_folder_map.get(folder.idx,{})

                )
            existing_folder_map[folder_hash] = existing_folder_obj
            
            
            
        # for folder_user in user_folder_mapping:
        #     existing_folder_obj: ExistingFolder = existing_folder_map.get(folder_hash)    
        #     existing_folder_obj.agent_users.add(folder_user.)
        #     existing_folder_obj.user_report_count_map[folder_user.]

        # 
        # for folder in existing_folder_list:
        #     folder_hash: str = folder.agent_id_path_hash
        #     existing_folder_obj: ExistingFolder = existing_folder_map.get(folder_hash)
        #     if existing_folder_obj:
        #         existing_folder_obj.agent_users.add(folder.agent_user_id)
        #         existing_folder_obj.user_report_count_map[folder.agent_user_id] = folder.report_count
        #     else:
        #         existing_folder_map[folder_hash]= ExistingFolder(
        #             idx = folder.idx,
        #             agent_id_path_hash = folder_hash,
        #             agent_users=set([folder.agent_user_id]),
        #             user_report_count_map={folder.agent_user_id : folder.report_count}

        #         )
        self.existing_folder_map = existing_folder_map
        t2=time()
        print("folder time",t2-t1)
        
    def add_folder_user_mapping(self,incoming_folder: IncomingFolder,existing_folder: Optional[ExistingFolder]=None):
        if existing_folder:
            folder_users_to_be_added: List[int] = incoming_folder.agent_users - existing_folder.agent_users
        else:
            folder_users_to_be_added: List[int] = incoming_folder.agent_users
        for agent_user_id in folder_users_to_be_added:
            if agent_user_id in self.folder_user_mapping_to_be_inserted:
                self.folder_user_mapping_to_be_inserted[agent_user_id].add(incoming_folder.agent_id_path_hash)
            else:
                self.folder_user_mapping_to_be_inserted[agent_user_id] = set([incoming_folder.agent_id_path_hash])
    
    def add_report_user_mapping(self,*, incoming_report: IncomingReport, existing_report: Optional[ExistingReport]=None):
        if existing_report:
            report_users_to_be_added: List[int] = incoming_report.agent_users - existing_report.agent_users
        else:
            report_users_to_be_added: List[int] = incoming_report.agent_users
        for agent_user_id in report_users_to_be_added:
            if agent_user_id in self.report_user_mapping_to_be_inserted:
                self.report_user_mapping_to_be_inserted[agent_user_id].add(incoming_report.reportid_agentid_path_hash)
            else:
                self.report_user_mapping_to_be_inserted[agent_user_id] = set([incoming_report.reportid_agentid_path_hash])
    


    def add_existing_folder_user(self,incoming_folder: IncomingFolder,existing_folder: ExistingFolder):
        folder_users_to_be_added: List[int] = incoming_folder.agent_users - existing_folder.agent_users
        for agent_user_id in folder_users_to_be_added:
            if agent_user_id in self.existing_folder_user_to_be_inserted:
                self.existing_folder_user_to_be_inserted[agent_user_id].add(existing_folder.idx)
            else:
                self.existing_folder_user_to_be_inserted[agent_user_id] = set([existing_folder.idx])
                # elif index == 0:
                #     #updating report count for added report
                #     folder_id: int = existing_folder_obj.idx
                #     current_report_user_count: int = existing_folder_obj.user_report_count_map[agent_user_id]
                    
                #     if agent_user_id in self.folder_user_report_count_update:
                #         folder_user_report_count: dict[int,int] = self.folder_user_report_count_update[agent_user_id].get(folder_id,{folder_id:current_report_user_count}) 
                #         folder_user_report_count[folder_id] += 1
                #     else:
                #         self.folder_user_report_count_update[agent_user_id] = {folder_id:current_report_user_count + 1}
               

    def add_incoming_folder_user(self,incoming_folder: IncomingFolder):
        for agent_user_id in incoming_folder.agent_users:
            if agent_user_id in self.incoming_folder_user_to_be_inserted:
                self.incoming_folder_user_to_be_inserted[agent_user_id].add(incoming_folder.agent_id_path_hash)
            else:
                self.incoming_folder_user_to_be_inserted[agent_user_id] = set([incoming_folder.agent_id_path_hash])
            
    
    
        
    def add_existing_report_user(self,*, incoming_report: IncomingReport, existing_report: ExistingReport):
        report_users_to_be_added: List[int] = incoming_report.agent_users - existing_report.agent_users
        for agent_user_id in report_users_to_be_added:
            if agent_user_id in self.existing_report_user_to_be_inserted:
                self.existing_report_user_to_be_inserted[agent_user_id].add(existing_report.idx)
            else:
                self.existing_report_user_to_be_inserted[agent_user_id] = set([existing_report.idx])
        
            
    
    def add_incoming_report_user(self,*, incoming_report: IncomingReport):
        for agent_user_id in incoming_report.agent_users:
            if agent_user_id in self.incoming_report_user_to_be_inserted:
                self.incoming_report_user_to_be_inserted[agent_user_id].add(incoming_report.reportid_agentid_path_hash)
            else:
                self.incoming_report_user_to_be_inserted[agent_user_id] = set([incoming_report.reportid_agentid_path_hash])
       
    
    def delete_report_user_mapping(self, incoming_report: IncomingReport, existing_report: ExistingReport):
        report_users_to_be_deleted: set[int] = existing_report.agent_users - incoming_report.agent_users
        for agent_user_id in report_users_to_be_deleted:
            if agent_user_id in self.report_user_mapping_to_be_deleted:
                self.report_user_mapping_to_be_deleted[agent_user_id].add(existing_report.idx)
            else:
                self.report_user_mapping_to_be_deleted[agent_user_id] = set([existing_report.idx])
    
        if self.is_admin_sync and len(report_users_to_be_deleted)==len(existing_report.agent_users):
            self.reports_to_be_deleted.add(existing_report.idx)

    def delete_folder_user_mapping(self, incoming_folder: IncomingFolder, existing_folder: ExistingFolder):
        folder_users_to_be_deleted: set[int] = existing_folder.agent_users - incoming_folder.agent_users
        for agent_user_id in folder_users_to_be_deleted:
            if agent_user_id in self.folder_user_mapping_to_be_deleted:
                self.folder_user_mapping_to_be_deleted[agent_user_id].add(existing_folder.idx)
            else:
                self.folder_user_mapping_to_be_deleted[agent_user_id] = set([existing_folder.idx])

        if self.is_admin_sync and len(folder_users_to_be_deleted)==len(existing_folder.agent_users):
            self.reports_to_be_deleted.add(existing_folder.idx)
            # need to remove folder user mappings

            # for index, report_folder_name in enumerate(report_folder_path_list):
            #     depth: int = len(report_folder_path_list) - index
            #     path: str = path_delimiter.join(report_folder_path_list[:index+1][::-1]) + path_delimiter
            #     agent_id_path_hash: str = sha1( "_".join([str(agent_id), path ]).encode()).hexdigest()
            #     existing_folder_obj: ExistingFolder = existing_folder_map[agent_id_path_hash]
            #     if index == 0:
            #         if agent_user_id in folder_user_report_count_update:
            #             user_report_count: int = existing_folder_obj.user_report_count_map[agent_user_id]
            #             folder_id: int = existing_folder_obj.idx
            #             folder_user_report_count: dict[int,int] =folder_user_report_count_update[agent_user_id].get(folder_id,{folder_id:user_report_count}) 
            #             folder_user_report_count[folder_id] -= 1
                

            #     if agent_user_id not in existing_folder_obj.agent_users:
            #         folder_user_mapping_to_be_inserted.get(agent_user_id,set()).add(existing_folder_obj.idx)
            #     else:
            #         break
                
    # def add_folders_for_report(self, incoming_report: IncomingReport) :
    #     report_folder_path_list: str = incoming_report.path.rstrip(codes.path_delimiter).split(codes.path_delimiter)
    #     for index, report_folder_name in enumerate(report_folder_path_list[::-1]):
    #         depth: int = len(report_folder_path_list) - index
    #         path: str = codes.path_delimiter.join(report_folder_path_list[:depth]) + codes.path_delimiter
    #         agent_id_path_hash: str = sha1( "_".join([str(self.agent_id), path ]).encode()).hexdigest()
            
    #         if agent_id_path_hash not in self.existing_folder_map and agent_id_path_hash not in self.folders_to_be_inserted.get(depth,()):
    #             report_folder_obj: InsertFolders = InsertFolders.construct(
    #                     name = report_folder_name,
    #                     path = path,
    #                     agent_id = self.agent_id,
    #                     depth = depth,
    #                     agent_id_path_hash = agent_id_path_hash,
    #                     sync_id = self.sync_id,        
                    
    #                 )
    #             if depth == codes.FOLDER_ROOT_LEVEL_DEPTH :
    #                 report_folder_obj.source_folder_id = None
    #             else:
    #                 source_folder_path: str = report_folder_obj.path[:-len(f'{report_folder_obj.name}{codes.path_delimiter}')]
    #                 source_folder_hash: str = sha1( "_".join([str(self.agent_id), source_folder_path ]).encode()).hexdigest() 
    #                 existing_source_folder: ExistingFolder = self.existing_folder_map.get(source_folder_hash)
                    
    #                 if existing_source_folder:
    #                     report_folder_obj.source_folder_id = existing_source_folder.idx
    #                 else:
    #                     report_folder_obj.source_folder_hash = source_folder_hash
                    
    #             if depth not in self.folders_to_be_inserted:
    #                 self.folders_to_be_inserted[depth] = {agent_id_path_hash:report_folder_obj}
    #             else:
    #                 self.folders_to_be_inserted[depth][agent_id_path_hash] = report_folder_obj
    #         else:
    #             break       

    def add_folder(self, incoming_folder: IncomingFolder) :
        depth: int = incoming_folder.depth
        if depth not in self.folders_to_be_inserted:
            self.folders_to_be_inserted[depth] = set([incoming_folder.agent_id_path_hash])
        else:
            self.folders_to_be_inserted[depth].add(incoming_folder.agent_id_path_hash)
          
    
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
        folder_hash_id_map: dict[str,int] = {}
        for depth in sorted(self.folders_to_be_inserted):
            folder_list: List[dict] = []
            for folder_hash in self.folders_to_be_inserted[depth]:
                source_folder_id: Optional[int] = None
                folder_obj: IncomingFolder =self.incoming_folder_map[folder_hash]
                if depth!=codes.FOLDER_ROOT_LEVEL_DEPTH:
                    existing_source_folder: ExistingFolder = self.existing_folder_map.get(folder_obj.source_folder_hash)
                    if existing_source_folder:
                        source_folder_id = existing_source_folder.idx
                    else:
                        source_folder_id = folder_hash_id_map[folder_obj.source_folder_hash]
                folder_list.append({"name":folder_obj.name,"source_folder_id":source_folder_id,"path":folder_obj.path,"agent_id":folder_obj.agent_id,"depth":folder_obj.depth,
                "agent_id_path_hash":folder_obj.agent_id_path_hash,"sync_id":self.sync_id,"created_by":self.user_id,"updated_by":self.user_id})   
                
            if folder_list:    
                bi_folder.create_folders(self.db,folder_list=folder_list)
                inserted_folders = bi_folder.get_folders_by_sync_id(self.db,sync_id=self.sync_id, depth=depth)
                for folder in inserted_folders:
                    folder_hash_id_map[folder.agent_id_path_hash] = folder.idx
                
                
        return folder_hash_id_map

    def insert_reports(self, folder_hash_id_map: dict[str,int]):
        report_list = []
        report_hash_id_map: dict[str,int] = {}
        
        for report_hash in self.reports_to_be_inserted:
            report_obj =self.incoming_report_map[report_hash]
            report_list.append(
                {
                    "name": report_obj.name,
                    "bi_folder_id": folder_hash_id_map[report_obj.source_folder_hash],
                    "path": report_obj.path,
                    "agent_id": self.agent_id,
                    "url": report_obj.url,
                    # "url_t": report_obj.url_t,
                    "description": report_obj.description,
                    "reportid_agentid_path_hash": report_obj.reportid_agentid_path_hash,
                    "update_hash": report_obj.update_hash,
                    "sync_id": self.sync_id,
                    "status": codes.ENABLED,
                    "created_by": self.user_id,
                    "updated_by": self.user_id,
                }
            )
        if report_list:
            bi_report.insert_reports(self.db,report_list=report_list)    
            
            inserted_reports: List[BIReport] = bi_report.get_reports_by_sync_id(self.db,sync_id=self.sync_id)
            for report in inserted_reports:
                report_hash_id_map[report.reportid_agentid_path_hash] = report.idx
        return report_hash_id_map

    def insert_folder_users(self, folder_hash_id_map: dict[str,int] ):        
        insert_folder_users = []
        for agent_user_id,folder_hash_set in self.folder_user_mapping_to_be_inserted.items():
            for folder_hash in folder_hash_set:
                
                incoming_folder_obj: IncomingFolder = self.incoming_folder_map[folder_hash]
                existing_folder_obj: ExistingFolder = self.existing_folder_map.get(folder_hash)
                if existing_folder_obj:
                    folder_id: int = existing_folder_obj.idx
                else:
                    folder_id: int = folder_hash_id_map[folder_hash]

                insert_folder_users.append(
                    {
                        "agent_user_id": agent_user_id,
                        "bi_folder_id": folder_id,
                        "report_count": incoming_folder_obj.user_report_count_map[agent_user_id],
                        "status": codes.ENABLED,
                        "created_by": self.user_id,
                        "updated_by": self.user_id
                    }
                )
        # for agent_user_id,report_hash_set in self.incoming_folder_user_to_be_inserted.items():
        #     for folder_hash in report_hash_set:
        #         folder_id: int = folder_hash_id_map[folder_hash]
        #         incoming_folder_obj: IncomingFolder = self.existing_folder_map[folder_id]
        #         insert_folder_users.append(
        #             {
        #                 "agent_user_id": agent_user_id,
        #                 "bi_folder_id": folder_id,
        #                 "report_count": incoming_folder_obj.user_report_count_map[agent_user_id],
        #                 "status": codes.ENABLED,
        #                 "created_by": self.user_id,
        #                 "updated_by": self.user_id
        #             }
        #         )
        if insert_folder_users:
            user_bi_folder.insert_folder_users(self.db,folder_user_list=insert_folder_users)

    def insert_report_users(self, report_hash_id_map: dict[str,int] ):        
        insert_report_users = []
        for agent_user_id,report_hash_set in self.report_user_mapping_to_be_inserted.items():
            for report_hash in report_hash_set:
                
                existing_report_obj: ExistingReport = self.existing_report_map.get(report_hash)
                if existing_report_obj:
                    report_id: int = existing_report_obj.idx
                else:
                    report_id: int = report_hash_id_map[report_hash]
                insert_report_users.append(
                    {
                        "agent_user_id": agent_user_id,
                        "report_id": report_id,
                        "status": codes.ENABLED,
                        "created_by": self.user_id,
                        "updated_by": self.user_id
                    }
                )
        # for agent_user_id,report_hash_set in self.incoming_report_user_to_be_inserted.items():
        #     for report_hash in report_hash_set:
        #         report_id: int = report_hash_id_map[report_hash]
        #         insert_report_users.append(
        #             {
        #                 "agent_user_id": agent_user_id,
        #                 "report_id": report_id,
        #                 "status": codes.ENABLED,
        #                 "created_by": self.user_id,
        #                 "updated_by": self.user_id
        #             }
        #         )
        if insert_report_users:
            user_bi_report.insert_report_users(self.db,report_user_list=insert_report_users)


    def sync_agent_reports(self): 
        
        self.agent_user_id_list = agent_user.get_agent_user_list(self.db, agent_id =self.agent_id)
        self.generate_incoming_report_folder_aggregate(incoming_report_details=[(1,get_reports().get("reports"))]) 
        
        # worker: Worker = Worker(worker_count=2)
        # worker.add_job(self.generate_existing_report_aggregate)
        # worker.add_job(self.generate_existing_folder_aggregate)
        # worker.start()
        # self.generate_existing_report_aggregate()
        # self.generate_existing_folder_aggregate()
        
        for incoming_report_hash,incoming_report in self.incoming_report_map.items():           
            existing_report: ExistingReport = self.existing_report_map.get(incoming_report_hash)
            
            if existing_report:
                # self.add_existing_report_user(incoming_report=incoming_report,existing_report=existing_report)
                
                # self.delete_report_user_mapping(incoming_report=incoming_report,existing_report=existing_report)

                # have to update folder report count
                                      
                # have to update folder report count
                self.add_report_user_mapping(incoming_report=incoming_report,existing_report=existing_report)
                if incoming_report.update_hash != existing_report.update_hash:
                    self.reports_to_be_updated.add(existing_report.idx)
                self.delete_report_user_mapping(incoming_report=incoming_report,existing_report=existing_report)
            else:
                # report does not exist
                # self.add_incoming_report_user(incoming_report=incoming_report)
                self.add_report_user_mapping(incoming_report=incoming_report)
                self.reports_to_be_inserted.add(incoming_report_hash)
            
        for incoming_folder_hash,incoming_folder in self.incoming_folder_map.items():
            existing_folder: ExistingFolder = self.existing_folder_map.get(incoming_folder_hash)
            if existing_folder:
                # self.add_existing_folder_user(incoming_folder=incoming_folder,existing_folder=existing_folder)
                folder_report_count_update = set(existing_folder.user_report_count_map.items()) - set(incoming_folder.user_report_count_map.items())
                for agent_user_id,existing_report_count in folder_report_count_update:
                    updated_report_count: int = incoming_folder.user_report_count_map.get(agent_user_id,0)
                    if existing_folder.idx not in self.folder_user_report_count_update:
                        self.folder_user_report_count_update[existing_folder.idx] = {agent_user_id:updated_report_count }
                    else:
                        self.folder_user_report_count_update[existing_folder.idx][agent_user_id] = updated_report_count 
                
                self.add_folder_user_mapping(incoming_folder=incoming_folder,existing_folder=existing_folder)
                self.delete_folder_user_mapping(incoming_folder=incoming_folder,existing_folder=existing_folder)
                pass
            else:
                # self.add_incoming_folder_user(incoming_folder=incoming_folder)
                self.add_folder_user_mapping(incoming_folder=incoming_folder)
                self.add_folder(incoming_folder=incoming_folder)
                
            
        
        folder_hash_id_map: dict[str,int] = self.insert_folders()
        self.insert_folder_users(folder_hash_id_map=folder_hash_id_map)
        report_hash_id_map: dict[str,int] = self.insert_reports(folder_hash_id_map=folder_hash_id_map)
        self.insert_report_users(report_hash_id_map = report_hash_id_map)
        
        
        print("reports:",len(self.reports_to_be_inserted))
        print("folders:",len(self.folders_to_be_inserted))
        # print("existing report users:",len(self.existing_report_user_to_be_inserted))
        print("report users:",len(self.report_user_mapping_to_be_inserted.get(1,[])))
        # print("existing folder users:",len(self.existing_folder_user_to_be_inserted))
        print("folder users:",len(self.folder_user_mapping_to_be_inserted.get(1,[])))
        #print(len(self.folder_user_mapping_to_be_inserted))
        #print(len(self.report_user_mapping_to_be_inserted))

        # if folder_user_report_count[folder_id] == 0 :
        #     folder_user_mapping_to_be_removed.get(agent_user_id,set()).add(existing_folder_obj.idx)
        
                        