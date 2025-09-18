from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status, HTTPException, Request
from app.core.security import verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import Token,TokenData
from app.core.databases import get_db


security=HTTPBearer()

def create_access_token(data : dict,expires_delta : timedelta | None = None):
  to_encode=data.copy()
  if expires_delta:
    expire=datetime.utcnow() + expires_delta
  else:
    expire=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  
  # Use your custom structure with 'id' as main identifier
  to_encode.update({
    "exp": expire,
    "email": data.get("email"),
    "id": data.get("id")
  })
  encoded_jwt=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
  
  return encoded_jwt

def verify_access_token(token : str,credentials_exception):
  try:
    # JWT decode automatically validates expiration
    payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    email: str = payload.get("email")
    id: int = payload.get("id")
    
    if email is None or id is None:
      raise credentials_exception
      
    return TokenData(email=email, id=id)
  except JWTError as e:
    # This will catch expired tokens and other JWT errors
    print(f"JWT Error: {e}")  # For debugging
    raise credentials_exception


async def get_current_user(request:Request,credentials : HTTPAuthorizationCredentials = Depends(security),db : Session = Depends(get_db)):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
  
  if not credentials:
    raise credentials_exception
    
  token = credentials.credentials
  token_data = verify_access_token(token, credentials_exception)
  
  user = db.query(User).filter(User.id == token_data.id).first()
  if user is None:
      raise credentials_exception
      
  if not user.is_active:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Inactive user"
      )
      
  request.state.user = user
  return user
  
  



