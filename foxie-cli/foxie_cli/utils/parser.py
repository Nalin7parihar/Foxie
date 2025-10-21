from pydantic import BaseModel
from typing import List

class Field(BaseModel):
  name : str
  type : str
  

def parse_fields(fields_str : str)->List[Field]:
  Fields=[]
  
  field_pairs = fields_str.split(",")
  
  for pair in field_pairs:
    clean_pair = pair.strip()
    if not clean_pair:
      continue
    
    parts = clean_pair.split(":")
    if(len(parts)!=2):
      raise ValueError(f"Invalid field format: '{clean_pair}'. Expected 'name:type'.")
    
    name  = parts[0].strip()
    type_str = parts[1].strip()
    
    if not name or not type_str:
      raise ValueError(f"Invalid field format: '{clean_pair}'. Name and type cannot be empty.")
    
    parsed_fields = Field(name=name,type=type_str)
    Fields.append(parsed_fields)
    
  return Fields