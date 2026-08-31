from sqlalchemy import Integer, String, Column , ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class ApiKey(Base):
    __tablename__="api_keys"

    id=Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name=Column(String, nullable=False,)
    key_hash=Column(String,unique=True,nullable=False)
    status=Column(String, nullable=False, default="active " )
    prefix = Column(String, nullable=False)
    rate_limit = Column(Integer, nullable=False, default=100)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())