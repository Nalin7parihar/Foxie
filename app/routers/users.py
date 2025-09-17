from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.users import UserResponse,UserUpdate,UserUpdatePassword
from app.core.databases import get_db
from app.models.users import User
from app.services.auth import get_current_user
from app.core.security import verify_password,hash_password

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def read_me(current_user : User = Depends(get_current_user)):
  return current_user

@router.put("/update",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def update_me(user_update : UserUpdate, db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
  user_update = user_update.model_dump(exclude_unset=True)
  
  for key,value in user_update.items():
    setattr(current_user,key,value)
  
  db.commit()
  db.refresh(current_user)
  return current_user

@router.patch("/update_password",status_code=status.HTTP_200_OK,response_model=UserResponse)
async def update_password(password_update : UserUpdatePassword,db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
  if password_update.old_password == password_update.new_password:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="New password must be different from old password")
  if not verify_password(password_update.old_password,current_user.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password is incorrect")
  
  current_user.password = hash_password(password_update.new_password)
  db.commit()
  db.refresh(current_user)

  return {"detail": "Password updated successfully"}

@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(db:Session = Depends(get_db), current_user : User = Depends(get_current_user)):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
  
  db.delete(current_user)
  db.commit()
  
  return {"detail" : "User deleted Successfully"}