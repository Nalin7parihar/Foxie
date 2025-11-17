from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os

# --- IMPORT CONFIGURATION AND AI LOGIC ---
try:
    from app.core.config import config
    from app.core.generator import generate_crud_feature
    from app.core.models import GeneratedCode
except ImportError as e:
    print(f"ERROR: Failed to import core AI logic. Check your backend folder structure. Details: {e}")
    import sys
    sys.exit(1)


# --- FastAPI Application ---

class ScaffoldRequest(BaseModel):
    """The request body expected from the CLI."""
    project_name: str = Field(..., description="Name of the project.")
    resource: str = Field(..., description="Name of the CRUD resource.")
    fields_str: str = Field(..., description="Comma-separated fields string.")
    database_type: str = Field(default="sql", description="Database type: 'sql' or 'mongodb'")
    enable_auth: bool = Field(default=False, description="Enable authentication (User model, auth endpoints)")
    api_key: Optional[str] = Field(None, description="Google Gemini API key (optional if set in environment)")


app = FastAPI(
    title=config.title,
    description=config.description,
    version=config.version
)

@app.post("/scaffold", response_model=GeneratedCode)
async def scaffold_feature(request: ScaffoldRequest):
    """
    Main endpoint: Receives a scaffolding request, runs the AI logic,
    and returns the generated code.
    """
    print(f"Received request to scaffold '{request.resource}' for project '{request.project_name}'...")

    try:
        # --- CALL THE REAL AI GENERATOR ---
        print(f"Calling AI generation function (DB: {request.database_type}, Auth: {request.enable_auth})...")
        generated_code = generate_crud_feature(
            project_name=request.project_name,
            resource=request.resource,
            fields_str=request.fields_str,
            api_key=request.api_key,
            database_type=request.database_type,
            enable_auth=request.enable_auth
        )

        if not generated_code or not generated_code.files:
             print("Warning: AI generation returned empty result.")
             # Return an empty list or raise error, depending on desired behaviour
             return GeneratedCode(files=[]) # Return empty list

        print(f"Successfully generated {len(generated_code.files)} files. Sending response to CLI.")
        return generated_code

    except Exception as e:
        # Log the full error on the backend for debugging
        print(f"An unexpected error occurred during generation: {e}")
        # Optionally add more detailed traceback logging here
        # import traceback
        # print(traceback.format_exc())

        # Raise a user-friendly error to the CLI
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred in the AI service: {str(e)}"
        )


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# Optional: Add basic entry point if you ever run this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
