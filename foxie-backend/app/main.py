from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables (like GOOGLE_API_KEY) from .env file
load_dotenv()

# --- IMPORT THE REAL AI LOGIC ---
# Ensure these files exist in foxie-backend/app/core/ and foxie-backend/app/utils/
try:
    from app.core.generator import generate_crud_feature
    from app.core.models import GeneratedCode, CodeFile
except ImportError as e:
    print(f"ERROR: Failed to import core AI logic. Check your backend folder structure. Details: {e}")
    # Exit if core logic is missing, as the app cannot function
    import sys
    sys.exit(1)


# --- FastAPI Application ---

class ScaffoldRequest(BaseModel):
    """The request body expected from the CLI."""
    project_name: str = Field(..., description="Name of the project.")
    resource: str = Field(..., description="Name of the CRUD resource.")
    fields_str: str = Field(..., description="Comma-separated fields string.")

app = FastAPI(
    title="Foxie AI Backend",
    description="Handles the AI code generation logic for the Foxie CLI."
)

@app.post("/scaffold", response_model=GeneratedCode)
async def scaffold_feature(request: ScaffoldRequest):
    """
    Receives a scaffolding request, runs the REAL AI logic,
    and returns the generated code.
    """
    print(f"Received request to scaffold '{request.resource}' for project '{request.project_name}'...")

    try:
        # --- CALL THE REAL AI GENERATOR ---
        print("Calling AI generation function...")
        generated_code = generate_crud_feature(
            project_name=request.project_name,
            resource=request.resource,
            fields_str=request.fields_str
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
    port = int(os.getenv("PORT", 8000))
    # Allow connections from any host if running in a container, otherwise default to localhost
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=port)
