from pydantic import BaseModel, Field
from typing import List

class CodeFile(BaseModel):
    """Represents a single generated code file."""
    file_path: str = Field(
        ..., 
        description="The full path for the file, e.g., 'app/models/product.py'."
    )
    content: str = Field(
        ...,
        description="The complete, syntactically correct code content for the file."
    )
    description: str = Field(
        ...,
        description="A brief, one-sentence explanation of this file's purpose."
    )

class GeneratedCode(BaseModel):
    """Represents the complete set of files for a scaffolded feature."""
    files: List[CodeFile] = Field(
        ...,
        description="A list of all the code files required for the feature."
    )