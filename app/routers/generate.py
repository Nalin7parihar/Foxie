from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.generate import GenerateRequest,GenerateResponse
from app.services.llm import llm_service
from app.models.users import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/generate",tags=["Generate"])


@router.post("/",response_model=GenerateResponse,status_code=status.HTTP_200_OK)
async def generate_docstring(request : GenerateRequest,current_user:User = Depends(get_current_user)):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
  
  code_snippet = request.code
  docstring_type = request.type
  if not code_snippet.strip():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Code snippet cannot be empty")
  
  docstring = llm_service.generate_docstring(code_snippet,docstring_type)
  
  return GenerateResponse(docstring=docstring)