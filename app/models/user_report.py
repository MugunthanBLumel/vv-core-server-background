from sqlalchemy import Column, ForeignKey, Integer, Sequence

from app.conf import codes
from app.db.base_class import Base


class UserReport(Base):
    """Mapping between the user created folder and BI report/User CustomUrl to
    display in a hierarchy view"""

    __tablename__ = "user_report"  # type: ignore

    idx = Column("id", Integer, Sequence("user_report_id_seq"), primary_key=True)
    item_type = Column(Integer, nullable=False)
    item_id = Column(
        Integer, nullable=False
    )  # Either user_report.id/user_custom_url.id
    user_folder_id = Column(Integer, ForeignKey("user_folder.id"))
    status = Column(Integer, nullable=False, default=codes.ENABLED)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=codes.DEFAULT_TIME())

    def __init__(
        self,
        *,
        item_type: int,
        item_id: int,
        user_folder_id: int,
        created_by: int,
        updated_by: int
    ) -> None:
        self.item_type = item_type
        self.item_id = item_id
        self.user_folder_id = user_folder_id
        self.created_by = created_by
        self.updated_by = updated_by
