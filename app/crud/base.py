"""Base CRUD File """

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import time
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import Column, and_, func
from sqlalchemy.orm import Query, Session, noload

from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import distinct
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.sql.selectable import Alias

from app.conf import codes
from app.core.exception import DbException
from app.db.base_class import Base
from app.schemas.query import SearchQueryModel
from app.db.session import engine,SessionLocal,ScopedSession,ManagedSession
from threading import Thread
from app.core.worker import Worker
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randrange
from sqlalchemy import exc

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD Class

    Extends:
    -------
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]

    Arguments:
    ----------
        model: Model Clas
        schema: A Pydantic Schema model class
    """

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Arguments:
        ----------
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, search: SearchQueryModel) -> List[ModelType]:
        """Retrieves the records based on given attributes

        Parameters
        ----------
        search : SearchQueryModel
            Details of the entity and filters to apply on the database table
        count : bool, optional
            If true returns the count of record as result

        Returns
        -------
        List[ModelType]
            Model object of records in the database table
        """
        result: List[ModelType] = []
        self.create_query(search)
        result = self.query.all()
        return result

    def get_count(self, query_object: SearchQueryModel) -> int:
        """Retrieves the record count which matches for the given condition

        Parameters
        ----------
        query_object : SearchQueryModel
            Details of the entity and filters to apply on the database table

        Returns
        -------
        int
            Count of the records from the result
        """
        self.create_query(query_object)
        return self.query.session.execute(
            self.query.statement.with_only_columns(
                [func.count(query_object.search_column[0])]
            )
        ).scalar()

    def get_result_set_count(self, query_object: SearchQueryModel) -> int:
        """This method is used to determine how many rows the
            SQL statement would return

           This method finds the count by wraping whatever it is we are
           querying into a subquery, then counts the rows from that .

           Usage : Incase of situation where get_count cannot be used,
                   like where aggregate count(func.count()) cannot be used.

        Parameters
        ----------
        query_object : SearchQueryModel
            Details of the entity and filters to apply on the database table

        Returns
        -------
        int
            Count of the records from the result
        """
        self.create_query(query_object)
        return self.query.count()

    def get_first(self, search: SearchQueryModel) -> Optional[ModelType]:
        """Retrieves the first record which matches for the given condition

        Parameters
        ----------
        search : SearchQueryModel
            Details of the entity and filters to apply on the database table

        Returns
        -------
        ModelType
            Model object of record in the database table
        """
        self.create_query(search)
        return self.query.first()

    def create(
        self, db: Session, *, user_id: int, obj_in: CreateSchemaType
    ) -> ModelType:
        """Adds a new record in the database table

        Parameters
        ----------
        db : Session
            Database session object
        obj_in : CreateSchemaType
            Model object to insert into the table

        Returns
        -------
        ModelType
            Model object with inserted values in the database table
        Raises
        ------
            Raises exception and the transaction is rolledback
        """
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(
                **obj_in_data, created_by=user_id, updated_by=user_id
            )  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as identifier:
            logger.exception(identifier)
            db.rollback()
            raise Exception("Error occured while inserting data in the database")

    def bulk_core_insert(self,*,obj_in):
        # engine.execute(
        #     self.model.__table__.insert(),
        #     obj_in
        #     )
        try:
            db: Session= ScopedSession()
            db.bulk_insert_mappings(self.model,
            obj_in,return_defaults=False)
            db.commit()
            db.close()
        except Exception as identifier:
            db.rollback()
            db.close()
            raise identifier
    
    # def batch_insert(self,db, *,obj_in: Union[List[ModelType]], batch_limit: int = 1000) -> None:
    #     worker: Worker = Worker(worker_count=5)
    #     start,end = 0, len(obj_in)
    #     while start<end:
            
    #         limited_obj_in = obj_in[start:start+min(batch_limit,end-start)]
    #         worker.add_job(target=self.bulk_core_insert,kwargs={"obj_in": limited_obj_in})
    #         # self.bulk_core_insert(db,obj_in=limited_obj_in)
    #         start+=min(batch_limit,end-start)
    #     worker.start()
    #     db.close()
    #     db=ScopedSession()
    #     return db
        
    def batch_insert(self,db, *,obj_in: Union[List[ModelType]], batch_limit: int = 1000) -> None:
        try:
            start,end = 0, len(obj_in)
            future_map = {}
            future_list = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                while start<end:
                    
                    limited_obj_in = obj_in[start:start+min(batch_limit,end-start)]
                    future = executor.submit(self.bulk_core_insert,obj_in=limited_obj_in)
                    future_map[future] = (limited_obj_in,0)
                    future_list.append(future)
                    # self.bulk_core_insert(db,obj_in=limited_obj_in)
                    start+=min(batch_limit,end-start)
            
                while len(future_list):
                    try:
                        future = future_list.pop(0)       
                        future.result()   
                        future_map.pop(future) 
                    except exc.IntegrityError as identifier:
                        object_list,retry_count = future_map.pop(future)
                        if len(object_list)>1:
                            split_at =  len(object_list)//2
                            first_batch = object_list[:split_at]
                            second_batch = object_list[split_at:]
                            first_batch_future = executor.submit(self.bulk_core_insert,obj_in=first_batch)
                            second_batch_future = executor.submit(self.bulk_core_insert,obj_in=second_batch)
                            future_map[first_batch_future] = (first_batch,retry_count)
                            future_map[second_batch_future] = (second_batch,retry_count)
                            future_list.extend([first_batch_future,second_batch_future])
                    except exc.InternalError as identifier:
                        object_list,retry_count = future_map.pop(future)
                        if retry_count < codes.DEAD_LOCK_RETRY_LIMIT:
                            wait_time = randrange( 1,5 ) +  2*retry_count  
                            time.sleep( wait_time )
                            future = executor.submit(self.bulk_core_insert,obj_in=object_list)
                            future_map[future] = (object_list,retry_count+1)
                            future_list.append(future)

                        else:
                           raise identifier
        except DbException as identifier:
            logger.exception(identifier)
            raise DbException(
                "Error occured while inserting data in the database"
            )
        finally:
            db.close()
            db=ScopedSession()
            return db
    
    def batch_update(self,db, *,obj_in: Union[List[ModelType]], batch_limit: int = 1000) -> None:
        future_map = {}
        future_list = []
        try:
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                start,end = 0, len(obj_in)
                while start<end:
                    limited_obj_in = obj_in[start:start+min(batch_limit,end-start)]
                    future = executor.submit(self.bulk_core_update,obj_in=limited_obj_in)
                    future_map[future] = (limited_obj_in,0)
                    future_list.append(future)
                    #self.bulk_core_update(db,obj_in=limited_obj_in)
                    start+=min(batch_limit,end-start)
                
                try:
                    future = future_list.pop(0)       
                    future.result()   
                    future_map.pop(future)
                except exc.InternalError as identifier:
                        object_list,retry_count = future_map.pop(future)
                        if retry_count < codes.DEAD_LOCK_RETRY_LIMIT:
                            wait_time = randrange( 1,5 ) +  2*retry_count  
                            time.sleep( wait_time )
                            future = executor.submit(self.bulk_core_insert,obj_in=object_list)
                            future_map[future] = (object_list,retry_count+1)
                            future_list.append(future)
                        else:
                            raise identifier
        except DbException as identifier:
            logger.exception(identifier)
            raise DbException(
                "Error occured while inserting data in the database"
            )
        finally:
            db.close()
            db=ScopedSession()
            return db

        
    def bulk_core_update(self,*,obj_in):
        db: Session= ScopedSession()
        db.bulk_update_mappings(self.model,obj_in)
        db.commit()
        db.close()

    # def batch_update(self,db, *,obj_in: Union[List[ModelType]], batch_limit: int = 1000) -> None:
    #     worker: Worker = Worker(worker_count=5)
    #     start,end = 0, len(obj_in)
    #     while start<end:
    #         limited_obj_in = obj_in[start:start+min(batch_limit,end-start)]
    #         worker.add_job(target=self.bulk_core_update,kwargs={"obj_in": limited_obj_in})
    #         #self.bulk_core_update(db,obj_in=limited_obj_in)
    #         start+=min(batch_limit,end-start)
    #     worker.start()
    #     db.close()
    #     db=ScopedSession()
    #     return db
        

    def create_all(self, db: Session, *, obj_in: Union[List[ModelType]],return_defaults=False) -> None:
        """Adds new records in the database table

        Parameters
        ----------
        db : Session
            Database session object
        obj_in : List[ModelType]
            Model object list to insert into the table

        """
        
        # db.add_all(obj_in)
        pass
        
    def update(
        self,
        db: Session,
        filters: List[ColumnElement] = [],
        commit: bool = True,
        *,
        obj_in: Union[
            UpdateSchemaType,
            Dict[str, GenericFunction],
            Dict[Column, GenericFunction],
        ],
        user_id: int,
    ) -> None:
        """updates existing records which matches the provided filter,
        updates all record if filter is empty

        Parameters
        ----------
        db : Session
            Database session object
        obj_in : Union[ UpdateSchemaType,
                 Dict[str, GenericFunction],
                 Dict[Column, GenericFunction], ]
            data to be updated or generic function that will return dynamic data
            to update
        filters : List[ColumnElement], optional
            filter to perform update for, by default []
        commit : bool, optional
             flag to skip commit, by default True
        user_id : int
             user_id of the user performing update
        Raises
        ------
            Raises DbException and the transaction is rolledback
        """
        try:
            filters.append(self.model.status != codes.DELETED)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            db.query(self.model).filter(*filters).update(
                {
                    **update_data,
                    "updated_at": str(int(datetime.now(tz=timezone.utc).timestamp())),
                    "updated_by": user_id,
                },
                synchronize_session=False,
            )
            if commit:
                db.commit()
        except DbException as identifier:
            logger.exception(identifier)
            db.rollback()
            raise DbException(
                "Error occured while updating existing data in the database"
            )

    def update_obj(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update the record with the given model values

        Parameters
        ----------
        db : Session
            Database session object
        db_obj : ModelType
            Model object of record in database
        obj_in : Union[UpdateSchemaType, Dict[str, Any]]
            Model object with respective fields to update in the Database record

        Returns
        -------
        ModelType
            Model object of updated record from database
        Raises
        ------
            Raises DbException and the transaction is rolledback
        """
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except DbException as identifier:
            logger.exception(identifier)
            db.rollback()
            raise DbException("Error occured while updating data in the database")

    def remove(self, db: Session, *, id: int) -> None:
        """Removes a record from the database table

        Parameters
        ----------
        db : Session
            Database session object
        id : int
            Identifier of the record in table
        Raises
        ------
            Raises DbException and the transaction is rolledback
        """
        try:
            obj = db.query(self.model).get(id)
            db.delete(obj)
            db.commit()
        except DbException as identifier:
            logger.exception(identifier)
            db.rollback()
            raise DbException("Error occured while removing data from the database")

    def delete(self, db: Session, *, id: int) -> None:
        """Deletes a record in the database table by updating status to 500

        Parameters
        ----------
        db : Session
            Database session object
        id : int
            Identifier of the record in table
        Raises
        ------
            Raises DbException and the transaction is rolledback
        """
        try:
            obj = db.query(self.model).get(id)
            setattr(obj, "status", codes.DELETED)
            db.commit()
        except DbException as identifier:
            logger.exception(identifier)
            db.rollback()
            raise DbException("Error occured while deleting data in the database")

    def create_query(self, search_object: SearchQueryModel) -> None:
        """Construct the search query with related filters and relationship

        Parameters
        ----------
        search_object : SearchQueryModel
            Details of the entity, relationship and filter to structure the query

        Raises
        ------
        AttributeError
            Exception will be raised if entity does not have the attribute/mapping
        """
        target_column: List[ColumnElement] = [*search_object.search_column]
        if search_object.distinct_column:
            target_column.append(distinct(search_object.distinct_column))
        if search_object.function_column:
            target_column.extend(search_object.function_column)
        if not search_object.exclude_default_filter:
            search_object.filters.append(self.model.status != codes.DELETED)
        query: Query = (
            search_object.db.query(*target_column)
            .filter(*search_object.filters)
            .options(noload("*"), *search_object.load_options)
        )
        if search_object.join:
            for relation in search_object.join:
                query = query.join(
                    relation.model.name,
                    and_(
                        *relation.relationship,
                        relation.model.name.status != codes.DELETED,
                    ),
                    isouter=relation.is_left,
                )
        if search_object.group_by_column:
            self.validate_group_by_column(
                search_object.search_column, search_object.group_by_column
            )
            query = query.group_by(*search_object.group_by_column)
        if search_object.order_by_column:
            query = query.order_by(*search_object.order_by_column)
        if search_object.limit != -1:
            query = query.offset(search_object.skip)
            query = query.limit(search_object.limit)
        self.query = query

    def validate_group_by_column(
        self, search_column: List[ColumnElement], group_column: List[ColumnElement]
    ) -> None:
        """Validate the group column contains only the columns specified in the search

        Parameters
        ----------
        search_column : List[ColumnElement]
            Entity attributes to be searched from the database table
        group_column : List[ColumnElement]
            Entity attributes used to group the result from the database table
        """
        if len(search_column) != len(group_column):
            raise AttributeError(
                "Attribute missing/added additionally in group_by_column"
            )
        if not all([column in search_column for column in group_column]):
            raise AttributeError("Attribute does not exist in group_by_column")

    def create_subquery(self, search_object: SearchQueryModel) -> Alias:
        """Constructs the subquery with the given relationship and filter

        Parameters
        ----------
        search_object : SearchQueryModel
            Details of the entity and filters to apply on the database table

        Returns
        -------
        Select
            Query object which used to join with other table
        """
        self.create_query(search_object)
        return self.query.subquery()
