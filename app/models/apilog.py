from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.databases import Base

class ApiLog(Base):
  __tablename__="api_logs"
  
  id = Column(Integer, primary_key=True,index=True)
  user_id = Column(Integer,ForeignKey("users.id"),nullable=True)
  client_ip_address = Column(String)
  
  http_method = Column(String, nullable=False,index=True)
  endpoint = Column(String,nullable=False, index=True)
  status_code = Column(Integer,nullable=False,index=True)
  
  processing_time_ms = Column(Integer)
  