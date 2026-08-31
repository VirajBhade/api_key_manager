from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Usagelog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)

    api_key_id = Column(
        Integer,
        ForeignKey("api_keys.id"),
        nullable=False,
        index=True
    )

    endpoint = Column(String, nullable=False)

    method = Column(String, nullable=False)

    status_code = Column(Integer, nullable=False)

    response_time = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )