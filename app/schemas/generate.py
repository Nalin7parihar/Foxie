from pydantic import BaseModel

class GenerateRequest(BaseModel):
  code : str
  type : str
  
class GenerateResponse(BaseModel):
  docstring : str
  
  