from app.schemas.bi_folder import AgentFolders
from app.models.bi_folder import BIFolder
from app.models.user_folder import UserFolder
from sqlalchemy.sql.functions import random
from app.schemas.query import SearchQueryModel
from app.models.bi_report import BIReport
from app.models.user_bi_report import UserBIReport
from app.schemas.bi_report import AgentReports
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from loguru import logger
from sqlalchemy.orm import Session, session

from app.crud.crud_bi_folder import bi_folder
from app.api import deps
from app.api.router import TimedRoute
from app.api.api_v2.endpoints.user.report_response import get_reports
from hashlib import sha1
from app.crud.crud_bi_report import bi_report
from app.core.sync_reports import SyncReports
import time 
import random

router: APIRouter = APIRouter(route_class=TimedRoute)

def test_insert(db):
    report_list =[]
    t1=time.time()
    
    for i in range(20000):
        report = BIReport(
                    name = "mugu"+ str(i),
                    agent_id = 1,
                    bi_folder_id = 1,
                    path = "s",
                    url = "s",
                    description = "s",
                    reportid_agentid_path_hash = "s"*50+str(i),
                    update_hash = "ss",
                    created_by = 1,
                    updated_by = 1,
                        )
        report_list.append(report)
    bi_report.create_all(db,obj_in = report_list,return_defaults=True)
    t2=time.time()
    print(report_list[0].idx, t2-t1)

def test_select_insert(db):
    report_list =[]
    sync_id=random.randrange(0,1000000)
    t1=time.time()
    rl_hash= []
    for i in range(20000):
        report = dict(
                    name = "mugu"+str(i),
                    agent_id = 1,
                    bi_folder_id = 1,
                    path = "s",
                    url = "s",
                    description = "s",
                    reportid_agentid_path_hash = "s"*50+str(i),
                    update_hash = "ss",
                    created_by = 1,
                    updated_by = 1,
                    sync_id = sync_id
                        )
        report_list.append(report)
        rl_hash.append("s"*50+str(i))
    
    bi_report.create_all(db,obj_in = report_list,return_defaults=False)
    
    report_map = {}
    t2=time.time()
    print("insert complete",t2-t1)
    result = bi_report.get(
            SearchQueryModel(
                db,
                search_column=[BIReport.idx,BIReport.reportid_agentid_path_hash],
                filters=[BIReport.sync_id == sync_id]
            )
    )
    print("result len",len(result))
    for i in result:
        report_map[i.reportid_agentid_path_hash] = i.idx
    # while start< end:
    #     rl = rl_hash[start:start+min(limit,end - start)]
    #     result = bi_report.get(
    #         SearchQueryModel(
    #             db,
    #             search_column=[BIReport.idx,BIReport.reportid_agentid_path_hash],
    #             filters=[BIReport.reportid_agentid_path_hash.in_(rl)]
    #         )
    #     )
    #     start+=min(limit,end - start)
    
    #     for i in result:
            
    #         report_map[i.reportid_agentid_path_hash] = i.idx
    t2=time.time()
    print(report_map[report_list[0]["reportid_agentid_path_hash"]] , t2-t1,len(report_map))

@router.post("/sync", response_model=None)
def report_sync(
    db: Session = Depends(deps.get_db),
):
    
    SyncReports(db).sync_agent_reports()

@router.post("", response_model=None)
def report_sync(
    db: Session = Depends(deps.get_db),
):
    #agent id : list of agent user id
    request = {
        "1": [1,2,3],
        "2": [1,2,3]
    }
    
    # new, updated, revoked
    # unique report - report_id,agent_id,path hash
    #report_hash : report
    
    # existing_agent_user_reports_map = {}
    # existing_agent_user_reports_set = set()
    # incoming_report_map = {}
    # reports_to_be_inserted = []
    # reports_to_be_updated = []
    # reports_to_be_revoked = []
    # reports_to_be_readded = []
   
    # for agent_id,agent_user_id_list in request.items():
    #     for agent_user_id in agent_user_id_list:
    #         report_list = get_reports().get("reports")
    #         for report in report_list:
    #             print(report)
    #             # have to check if the report already exist for the user
    #             report_hash =  sha1( "_".join([report['report_id'], str(agent_id) , report['path'] ]).encode()).hexdigest()
    #             incoming_report_map[report_hash] = report
    #             if report_hash in existing_agent_user_reports_map:
    #                 update_hash =  sha1( "_".join([report['description']]).encode()).hexdigest()
    #                 existing_report = existing_agent_user_reports_map[report_hash]
    #                 if existing_report.status == 500:
    #                     reports_to_be_readded.append(report)
    #                 elif update_hash != existing_report.update_hash:
    #                     reports_to_be_updated.append(report)
                        
    #             else:
    #                 reports_to_be_inserted.append(report)
                
    #     incoming_report_set = set(incoming_report_map.keys())
    #     #revoke reports 
    #     for report in existing_agent_user_reports_set - incoming_report_set:
    #         reports_to_be_revoked.append(report)
   
    #test_insert(db)
    #test_select_insert(db)
    # test_parent(db)
    
    path_delimiter = "\\"
    ROOT_LEVEL_DEPTH = 1
    agent_id: int = 1
    user_id: int =1
    agent_user_id: int = 1
    sync_id: int = random.randrange(1,10000000)
    existing_agent_reports = []
    existing_agent_folders = []
    existing_report_map: dict[str, AgentReports] = {}
    existing_folder_map: dict[str, AgentFolders] = {}
    incoming_agent_user_reports = {1:get_reports().get("reports")}
    incoming_reports_map = {}
    existing_user_report_map: Dict[int,set[str]] = {}
    existing_user_folder_map: Dict[int,set[str]] = {}
    is_admin_sync: bool = True
    reports_to_be_inserted: dict[str,dict] = {}
    folders_to_be_inserted:dict[int,dict[str,dict]] = {}
    reports_to_be_updated = []
    report_user_to_be_inserted:list[dict] = []
    
    if is_admin_sync:
        existing_agent_reports: List[AgentReports] = bi_report.get_reports_by_agent_id(db,agent_id=agent_id)
        existing_agent_folders: List[AgentFolders] = bi_folder.get_folders_by_agent_id(db,agent_id=agent_id)
    else:
        existing_agent_reports: List[AgentReports] = bi_report.get_reports_by_agent_user_id(db,agent_user_id=agent_user_id)
        existing_agent_folders: List[AgentFolders] = bi_folder.get_folders_by_agent_user_id(db,agent_user_id=agent_user_id) 
    for report in existing_agent_reports:

        if is_admin_sync:
            agent_user_id = report.agent_user_id
        if agent_user_id in existing_user_report_map:
            existing_user_report_map[agent_user_id].add(report.reportid_agentid_path_hash)
        else:
            existing_user_report_map[agent_user_id] = set([report.reportid_agentid_path_hash])
        existing_report_map[report.reportid_agentid_path_hash] = report
    
    for folder in existing_agent_folders:
        if is_admin_sync:
            agent_user_id = folder.agent_user_id
        if agent_user_id in existing_user_folder_map:
            existing_user_folder_map[agent_user_id].add(folder.agent_id_path_hash)
        else:
            existing_user_folder_map[agent_user_id] = set([folder.agent_id_path_hash])
        existing_folder_map[folder.agent_id_path_hash] = folder

    for agent_user_id in incoming_agent_user_reports:
        
        for incoming_report in incoming_agent_user_reports[agent_user_id]:
            incoming_report_hash: str = sha1( "_".join([incoming_report['report_id'], str(agent_id) , report['path'] ]).encode()).hexdigest()
            
            existing_report = existing_report_map.get(incoming_report_hash)
            if existing_report:
                incoming_update_hash: str = sha1("_".join([ report["name"], report.get("description",""), report.get("url",""), report.get("meta","{}"), report.get("sync_metadata","{}") ]).encode()).hexdigest()
                if incoming_report_hash not in existing_user_report_map:
                    # report needs to be added for user
                    report_user_to_be_inserted.append(
                        {
                        "agent_id_path_hash": incoming_report_hash,
                        "agent_user_id": agent_user_id
                        }
                    )
                if incoming_update_hash!= existing_report.update_hash:
                    pass
            else:
                # report does not exist
                agent_id_path_hash: str = sha1( "_".join([str(agent_id), incoming_report["path"] ]).encode()).hexdigest()
                report_folder_path_list: str = incoming_report["path"].split(path_delimiter)
                if agent_id_path_hash not in existing_folder_map:
                    for index, report_folder_name in enumerate(report_folder_path_list):
                        depth: int = index + 1
                        path: str = path_delimiter.join(report_folder_path_list[:depth])
                        agent_id_path_hash: str = sha1( "_".join([str(agent_id), path ]).encode()).hexdigest()
                        if agent_id_path_hash not in existing_folder_map:

                            report_folder_obj: dict = {
                                "name" : report_folder_name,
                                "path" : path,
                                "agent_id" : agent_id,
                                "depth" : depth,
                                "sync_id": sync_id,
                                "agent_id_path_hash": agent_id_path_hash,
                                "created_by" : user_id,
                                "updated_by" : user_id,
                            }
                            if depth == ROOT_LEVEL_DEPTH :
                                report_folder_obj["source_folder_id"] = None
                            else:
                                parent_path: str = report_folder_obj["path"].rstrip(f'{report_folder_obj["name"]}{path_delimiter}')
                                parent_agent_id_path_hash: str = sha1( "_".join([str(agent_id), parent_path ]).encode()).hexdigest() 
                                existing_parent_folder: AgentFolders = existing_folder_map.get(parent_agent_id_path_hash)
                                
                                if existing_parent_folder:
                                    report_folder_obj["source_folder_id"] = existing_parent_folder.idx
                                else:
                                    report_folder_obj["parent_agent_id_path_hash"] = parent_agent_id_path_hash
                                if depth not in folders_to_be_inserted:
                                    folders_to_be_inserted[depth] = {agent_id_path_hash:report_folder_obj}
                                else:
                                    folders_to_be_inserted[depth][agent_id_path_hash] = report_folder_obj
                            

                reports_to_be_inserted[incoming_report_hash] = {
                            "name" : incoming_report["name"],
                            "agent_id" : incoming_report["agent_id"],
                            "path" : incoming_report["path"],
                            "url" : incoming_report["url"],
                            "description" : incoming_report["description"],
                            "reportid_agentid_path_hash" : incoming_report["reportid_agentid_path_hash"],
                            "update_hash" : incoming_update_hash}
                        
            
            for depth in sorted(folders_to_be_inserted):
                folders_to_be_inserted: List[dict] = []
                for report_folder_obj in folders_to_be_inserted[depth].values():
                    if "source_folder_id" not in report_folder_obj:
                        parent_agent_id_path_hash: str = report_folder_obj.pop("parent_agent_id_path_hash")
                        report_folder_obj["source_folder_id"] = folders_to_be_inserted[depth-1][parent_agent_id_path_hash].idx
                       
                                                                            
                bi_folder.create_folders(folder_list=folders_to_be_inserted[depth].values())
                for folder in bi_folder.get_folders_by_sync_id(db,sync_id=sync_id):
                    folders_to_be_inserted[depth][folder.agent_id_path_hash] = folder.idx

                    # report = BIReport(
                        #     name = incoming_report["name"],
                        #     agent_id = incoming_report["agent_id"],
                        #     bi_folder_id = bi_folder_id,
                        #     path = incoming_report["path"],
                        #     url = incoming_report["url"],
                        #     description = incoming_report["description"],
                        #     reportid_agentid_path_hash = incoming_report["reportid_agentid_path_hash"],
                        #     update_hash = incoming_update_hash
                        # )
                    # reports_to_be_inserted.append(report)
            
            

                    

    
    
    