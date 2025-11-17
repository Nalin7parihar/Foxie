import os
import typer
import re
from typing import List, Optional

def _optimize_example_content(content: str, filename: str) -> str:
    """
    Optimize example file content to reduce token usage:
    - Remove commented-out alternative implementations (e.g., # NOSQL VERSION)
    - Remove excessive whitespace
    - Keep only essential code and comments
    """
    lines = content.split('\n')
    optimized_lines = []
    skip_block = False
    
    for line in lines:
        # Skip large commented-out code blocks (alternative implementations)
        if re.match(r'^#\s*(NOSQL|SQL)\s+VERSION', line, re.IGNORECASE):
            skip_block = True
            continue
        if skip_block and line.strip() and not line.strip().startswith('#'):
            # Check if we've reached the end of the commented block
            if not line.strip().startswith('#') and line.strip():
                skip_block = False
        if skip_block:
            continue
            
        # Remove lines that are just "--- START/END" markers (we'll add our own)
        if re.match(r'^#\s*---\s*(START|END):', line):
            continue
            
        optimized_lines.append(line)
    
    # Join and clean up excessive blank lines (max 2 consecutive)
    result = '\n'.join(optimized_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()

def load_style_guide_snippets(
    base_dir: str = "data/rag_knowledge_base/fastapi",
    database_type: str = "sql",
    enable_auth: bool = False
) -> str:
    """
    Reads relevant .example files from the RAG knowledge base
    based on database type and auth requirements.
    Optimizes content to reduce token usage.
    
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
                    # Optimize content to reduce tokens
                    optimized_content = _optimize_example_content(content, filename)
                    # Add concise headers
                    snippets.append(f"# {filename}\n{optimized_content}")
                    
    except FileNotFoundError:
        # Don't fail the whole app, just warn the user
        typer.secho(f"Warning: RAG directory not found at {base_dir}. Skipping style guide.", fg=typer.colors.YELLOW)
        return ""
    
    return "\n\n".join(snippets)