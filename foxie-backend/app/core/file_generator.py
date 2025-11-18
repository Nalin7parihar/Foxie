"""
File generation logic for individual file generation.
Generates each file type with appropriate prompts and RAG integration.
Note: Currently not used in standard mode, but available for future use.
"""
from typing import Dict, List, Optional
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


class FileGenerator:
    """Generates individual files with context-aware prompts."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        # Use gemini-1.5-flash for better free tier limits
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
    def _load_rag_examples(self, file_type: str) -> str:
        """Load relevant examples from RAG knowledge base."""
        rag_dir = "data/rag_knowledge_base/fastapi"
        file_map = {
            "config": "config.py.example",
            "db_session": "db_session.py.example",
            "base_model": "base_model.py.example",
            "auth_dependency": "auth_dependency.py.example",
            "main": "main.py.example"
        }
        
        example_file = file_map.get(file_type)
        if not example_file:
            return ""
        
        example_path = os.path.join(rag_dir, example_file)
        if os.path.exists(example_path):
            with open(example_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def generate_config_file(self, project_name: str) -> str:
        """Generate app/core/config.py"""
        example = self._load_rag_examples("config")
        
        prompt = f"""Generate a production-ready FastAPI configuration file.

Project: {project_name}

Requirements:
- Use Pydantic Settings for environment variables
- Include DATABASE_URL with proper validation
- Add SECRET_KEY for JWT
- Include CORS_ORIGINS as a list
- Add PROJECT_NAME and VERSION
- Use proper type hints

Example reference (adapt as needed):
{example}

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_db_session_file(self, project_name: str) -> str:
        """Generate app/database/db_session.py"""
        example = self._load_rag_examples("db_session")
        
        prompt = f"""Generate a database session file using SQLAlchemy 2.0+.

Project: {project_name}

Requirements:
- Use SQLAlchemy 2.0 async syntax
- Import settings from app.core.config
- Create async engine and sessionmaker
- Include get_db() dependency for FastAPI
- Use proper type hints
- Add connection pooling configuration

Example reference (adapt as needed):
{example}

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_base_model_file(self, project_name: str) -> str:
        """Generate app/models/base_model.py"""
        example = self._load_rag_examples("base_model")
        
        prompt = f"""Generate a SQLAlchemy base model class.

Project: {project_name}

Requirements:
- Use SQLAlchemy 2.0+ syntax with Mapped[] type hints
- Include id, created_at, updated_at fields
- Use mapped_column() for column definitions
- Make it a declarative base class
- Add __repr__ method
- Use proper imports from sqlalchemy.orm

Example reference (adapt as needed):
{example}

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_resource_model_file(
        self, 
        project_name: str, 
        resource_name: str, 
        fields: List[Dict[str, str]]
    ) -> str:
        """Generate app/models/{resource}.py"""
        
        fields_str = "\n".join([
            f"- {f['name']}: {f['type']}" for f in fields
        ])
        
        prompt = f"""Generate a SQLAlchemy model for the resource '{resource_name}'.

Project: {project_name}
Resource: {resource_name}
Fields:
{fields_str}

Requirements:
- Inherit from BaseModel (imported from app.models.base_model)
- Use SQLAlchemy 2.0+ syntax with Mapped[] type hints
- Use mapped_column() for all fields
- Set proper __tablename__
- Map Python types to SQLAlchemy types:
  * str → String
  * int → Integer
  * float → Float
  * bool → Boolean
  * datetime → DateTime
- Add proper imports
- Include __repr__ method

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_schema_file(
        self, 
        project_name: str, 
        resource_name: str, 
        fields: List[Dict[str, str]]
    ) -> str:
        """Generate app/schemas/{resource}.py"""
        
        fields_str = "\n".join([
            f"- {f['name']}: {f['type']}" for f in fields
        ])
        
        prompt = f"""Generate Pydantic schemas for the resource '{resource_name}'.

Project: {project_name}
Resource: {resource_name}
Fields:
{fields_str}

Requirements:
- Create 3 schema classes:
  1. {resource_name.capitalize()}Base: Shared properties
  2. {resource_name.capitalize()}Create: For POST requests (no id)
  3. {resource_name.capitalize()}Response: For responses (includes id, created_at, updated_at)
- Use Pydantic BaseModel
- Add proper type hints
- Use ConfigDict with from_attributes=True for Response schema
- Add Field(...) with descriptions where appropriate

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_crud_file(
        self, 
        project_name: str, 
        resource_name: str, 
        fields: List[Dict[str, str]]
    ) -> str:
        """Generate app/crud/{resource}.py"""
        
        prompt = f"""Generate CRUD operations for the resource '{resource_name}'.

Project: {project_name}
Resource: {resource_name}

Requirements:
- Create a CRUDManager class
- Use SQLAlchemy 2.0 async syntax
- Import the model from app.models.{resource_name}
- Import AsyncSession from sqlalchemy.ext.asyncio
- Implement these methods:
  * async def create() - Insert new record
  * async def get_by_id() - Fetch by primary key
  * async def get_all() - Fetch all with pagination
  * async def update() - Update existing record
  * async def delete() - Delete record
- Use select(), session.execute(), session.commit()
- Add proper type hints
- Handle exceptions gracefully

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_endpoint_file(
        self, 
        project_name: str, 
        resource_name: str, 
        fields: List[Dict[str, str]]
    ) -> str:
        """Generate app/api/endpoints/{resource}.py"""
        
        prompt = f"""Generate FastAPI endpoint routes for the resource '{resource_name}'.

Project: {project_name}
Resource: {resource_name}

Requirements:
- Create an APIRouter with prefix="/{resource_name}s" and tag=["{resource_name}s"]
- Import schemas from app.schemas.{resource_name}
- Import CRUDManager from app.crud.{resource_name}
- Import get_db dependency from app.database.db_session
- Implement these endpoints:
  * POST /{resource_name}s - Create new (returns 201)
  * GET /{resource_name}s - List all with pagination
  * GET /{resource_name}s/{{id}} - Get by ID (returns 404 if not found)
  * PUT /{resource_name}s/{{id}} - Update (returns 404 if not found)
  * DELETE /{resource_name}s/{{id}} - Delete (returns 204)
- Use proper status codes from fastapi.status
- Add response_model to endpoints
- Use Depends() for database session injection
- Add docstrings to each endpoint

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_router_file(
        self, 
        project_name: str, 
        resource_name: str
    ) -> str:
        """Generate app/api/router.py"""
        
        prompt = f"""Generate the API router aggregation file.

Project: {project_name}
Resource: {resource_name}

Requirements:
- Create a main APIRouter
- Import the {resource_name} endpoint router
- Include the {resource_name} router in the main router
- Add prefix="/api/v1" to the main router
- Keep it extensible for adding more routers later

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_auth_dependency_file(self, project_name: str) -> str:
        """Generate app/dependencies/auth_dependency.py"""
        example = self._load_rag_examples("auth_dependency")
        
        prompt = f"""Generate an authentication dependency for FastAPI.

Project: {project_name}

Requirements:
- Create a simple get_current_user() dependency
- Use OAuth2PasswordBearer
- Return a placeholder user for now (can be enhanced later)
- Add proper type hints
- Include docstring

Example reference (adapt as needed):
{example}

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_main_file(
        self, 
        project_name: str, 
        resource_name: str
    ) -> str:
        """Generate app/main.py"""
        example = self._load_rag_examples("main")
        
        prompt = f"""Generate the FastAPI application entry point.

Project: {project_name}
Resource: {resource_name}

Requirements:
- Create FastAPI app instance with title and version
- Import settings from app.core.config
- Import api_router from app.api.router
- Include the api_router
- Add CORS middleware with allowed origins from config
- Add a root endpoint GET / returning {{"message": "Welcome to {project_name}"}}
- Add proper imports
- Keep it clean and production-ready

Example reference (adapt as needed):
{example}

Generate ONLY the Python code, no markdown, no explanations."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        return response.text.strip()
    
    def generate_file(
        self, 
        file_path: str, 
        project_name: str, 
        resource_name: str, 
        fields: List[Dict[str, str]],
        context: Dict[str, str] = None
    ) -> str:
        """
        Main entry point for file generation.
        Routes to appropriate generator based on file path.
        """
        
        if "config.py" in file_path:
            return self.generate_config_file(project_name)
        
        elif "db_session.py" in file_path:
            return self.generate_db_session_file(project_name)
        
        elif "base_model.py" in file_path:
            return self.generate_base_model_file(project_name)
        
        elif f"models/{resource_name}.py" in file_path:
            return self.generate_resource_model_file(project_name, resource_name, fields)
        
        elif f"schemas/{resource_name}.py" in file_path:
            return self.generate_schema_file(project_name, resource_name, fields)
        
        elif f"crud/{resource_name}.py" in file_path:
            return self.generate_crud_file(project_name, resource_name, fields)
        
        elif f"endpoints/{resource_name}.py" in file_path:
            return self.generate_endpoint_file(project_name, resource_name, fields)
        
        elif "router.py" in file_path:
            return self.generate_router_file(project_name, resource_name)
        
        elif "auth_dependency.py" in file_path:
            return self.generate_auth_dependency_file(project_name)
        
        elif "main.py" in file_path:
            return self.generate_main_file(project_name, resource_name)
        
        else:
            raise ValueError(f"Unknown file type: {file_path}")
