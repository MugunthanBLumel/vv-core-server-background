from typing import Callable, Generic, List, NamedTuple, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement, ColumnElement

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class Model(Generic[ModelType]):
    """A class to define the entity type"""

    def __init__(self, model: Type[ModelType]) -> None:
        """Initialize the entity and its type

        Parameters
        ----------
        model : Type[ModelType]
            Entity name to be searched
        """
        self.name = model


class JoinModel(NamedTuple):
    """A class to define the model and its relationship to join on the query"""

    model: Model
    relationship: List[Union[ClauseElement, str, bool]]
    is_left: bool = False


class SearchQueryModel(NamedTuple):
    """A class to define the attributes to perform the search query"""

    db: Session
    search_column: List[ColumnElement]
    function_column: List[ColumnElement] = []
    distinct_column: Optional[ColumnElement] = None
    load_options: List[Callable] = []
    filters: List[ColumnElement] = []
    exclude_default_filter: bool = False
    join: List[JoinModel] = []
    group_by_column: List[ColumnElement] = []
    order_by_column: List[ColumnElement] = []
    skip: int = 0
    limit: int = -1
