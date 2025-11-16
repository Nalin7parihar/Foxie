import os
import typer
from typing import List, Optional

def load_style_guide_snippets(
    base_dir: str = "data/rag_knowledge_base/fastapi",
    database_type: str = "sql",
    enable_auth: bool = False
) -> str:
    """
    Reads relevant .example files from the RAG knowledge base
    based on database type and auth requirements.
    
    Args:
        base_dir: Base directory for RAG examples
        database_type: "sql" or "mongodb"
        enable_auth: Whether to include auth examples
    """
    snippets: List[str] = []
    
    # Core files that are always included
    core_files = [
        "config.py.example",
        "main.py.example",
    ]
    
    # Database-specific files
    if database_type == "mongodb":
        db_files = [
            "db_session_mongodb.py.example",
            "base_model_mongodb.py.example",
        ]
    else:  # sql
        db_files = [
            "db_session.py.example",
            "base_model.py.example",
        ]
    
    # Auth files (if enabled)
    auth_files = []
    if enable_auth:
        auth_files = [
            "auth_dependency.py.example",
            "security.py.example",
            "user_model.py.example",
            "auth_endpoints.py.example",
        ]
    
    # Combine all files
    files_to_load = core_files + db_files + auth_files
    
    try:
        # Load only the relevant files
        for filename in files_to_load:
            file_path = os.path.join(base_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Add headers to help the AI distinguish between files
                    snippets.append(f"--- START: {filename} ---\n{content}\n--- END: {filename} ---")
                    
    except FileNotFoundError:
        # Don't fail the whole app, just warn the user
        typer.secho(f"Warning: RAG directory not found at {base_dir}. Skipping style guide.", fg=typer.colors.YELLOW)
        return ""
    
    return "\n\n".join(snippets)