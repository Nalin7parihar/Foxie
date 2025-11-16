"""
Standard mode code generator - one-shot generation.
Uses Google Gemini with RAG for fast prototyping.
"""
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
from app.utils.rag import load_style_guide_snippets
from app.core.prompts import MASTER_PROMPT_TEMPLATE
from app.core.models import GeneratedCode
from app.utils.parser import parse_fields, Field
from app.utils.api_key_manager import APIKeyManager
from typing import List, Optional

load_dotenv()


def generate_crud_feature(
    resource: str,
    fields_str: str,
    project_name: str,
    api_key: Optional[str] = None,
    database_type: str = "sql",
    enable_auth: bool = False,
    protect_routes: bool = False
) -> GeneratedCode:
    """
    Generate a complete CRUD feature in one shot (Standard mode).
    
    Args:
        resource: Name of the resource (e.g., "product", "user")
        fields_str: Comma-separated fields (e.g., "name:str,price:float")
        project_name: Name of the project
        api_key: Optional Google Gemini API key
        database_type: "sql" or "mongodb"
        enable_auth: Whether to generate authentication (User model, auth endpoints)
        protect_routes: Whether to protect resource routes with authentication
        
    Returns:
        GeneratedCode with all files
        
    Raises:
        ValueError: If API key is missing or invalid
        Exception: If generation fails
    """
    # Get API key using centralized manager
    resolved_key = APIKeyManager.get_api_key(
        provided_key=api_key,
        raise_if_missing=True
    )
    
    # Initialize Gemini client
    client = genai.Client(api_key=resolved_key)
    
    # Parse fields
    parsed_fields: List[Field] = []
    try:
        parsed_fields = parse_fields(fields_str)
    except Exception as e:
        raise ValueError(f"Error parsing fields: {e}")
    
    fields_list_str = "\n".join([f"- **{f.name}**: {f.type}" for f in parsed_fields])
    
    # Validate database type
    if database_type not in ["sql", "mongodb"]:
        raise ValueError(f"Invalid database_type: {database_type}. Must be 'sql' or 'mongodb'")
    
    # Load RAG knowledge base based on database type and auth
    print(f"📚 Loading style guide snippets from RAG knowledge base (DB: {database_type}, Auth: {enable_auth})...")
    style_guide = load_style_guide_snippets(
        database_type=database_type,
        enable_auth=enable_auth
    )
    
    # Build database-specific instructions
    if database_type == "sql":
        database_type_instructions = "Use SQLAlchemy 2.0 with Mapped[] type hints and mapped_column()"
        database_specific_instructions = """
For SQL databases:
- Use SQLAlchemy 2.0+ syntax with `Mapped[]` type hints
- Use `mapped_column()` for column definitions
- Models inherit from `Base` (DeclarativeBase)
- Use `Session` from SQLAlchemy for database operations
- Use `select()` statements or `session.query()`
"""
    else:  # mongodb
        database_type_instructions = "Use MongoDB with Beanie ODM or Motor async driver"
        database_specific_instructions = """
For MongoDB databases:
- Use Beanie Document syntax or Motor async client
- Models inherit from `BaseDocument` (Beanie Document)
- Use `AsyncIOMotorClient` for database operations
- Use async/await for all database operations
- Collections are accessed via `db.collection_name`
"""
    
    # Build auth-specific instructions
    if enable_auth:
        auth_specific_instructions = f"""
Authentication is ENABLED. You MUST generate:
1. app/core/security.py - Password hashing and JWT utilities
2. app/models/user.py - User model ({database_type})
3. app/schemas/user.py - User schemas (UserCreate, UserResponse, Token, Login)
4. app/crud/user.py - User CRUD with password hashing
5. app/api/endpoints/auth.py - Registration and login endpoints
6. app/dependencies/auth_dependency.py - JWT token validation

Protected Routes: {protect_routes}
- If protect_routes=True: Resource endpoints (POST, PUT, DELETE) MUST require authentication
- If protect_routes=False: Resource endpoints are public (auth is optional)
- Auth endpoints (/auth/register, /auth/login, /auth/me) are always available when auth is enabled
"""
    else:
        auth_specific_instructions = "Authentication is DISABLED. Do not generate auth-related files."
    
    # Build prompt
    prompt = MASTER_PROMPT_TEMPLATE.format(
        resource=resource,
        fields_list=fields_list_str,
        project_name=project_name,
        style_guide=style_guide,
        database_type=database_type,
        database_type_instructions=database_type_instructions,
        database_specific_instructions=database_specific_instructions,
        enable_auth=str(enable_auth),
        protect_routes=str(protect_routes),
        auth_specific_instructions=auth_specific_instructions
    )
    
    # Generate code
    print("🤖 Generating CRUD feature using Gemini model...")
    try:
        # Use gemini-1.5-flash for better free tier limits
        # Can be overridden via GEMINI_MODEL environment variable
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": GeneratedCode
            }
        )
        
        print("✅ Received response from Gemini model")
        return response.parsed
        
    except Exception as e:
        raise Exception(f"Error generating CRUD feature: {e}")
  

