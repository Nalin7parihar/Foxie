from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
from sqlalchemy.orm import Session
from app.core.databases import get_db_session
from app.models.apilog import ApiLog


class LogMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request:Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    processing_time_ms = (time.time() - start_time)*1000
    
    with get_db_session() as db:
      user_id = request.state.user.id if hasattr(request.state, "user") else None
      
      log_entry = ApiLog(
        http_method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
        client_ip_address=request.client.host,
        processing_time_ms=int(processing_time_ms),
        user_id=user_id
      )
      
      db.add(log_entry)
      db.commit()
    return response