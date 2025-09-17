from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate,UserResponse,UserLogin,Token
from app.core.databases import get_db
from app.models.users import User
from app.services.auth import create_access_token
from app.core.security import verify_password,hash_password

router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user : UserCreate, db : Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()
  if db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
  
  hashed_password = hash_password(user.password)
  user.password = hashed_password
  user_data = user.model_dump()
  db_user = User(**user_data)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  
  return db_user

@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login(user : UserLogin, db : Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()
  if not db_user or not verify_password(user.password,db_user.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
  
  access_token = create_access_token(data={"email":db_user.email,"id":db_user.id})
  
  return {"access_token":access_token,"token_type":"bearer"}