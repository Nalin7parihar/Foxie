"""
Static template generator for pyproject.toml and .env files.
These are generated as static files (not AI-generated) for consistency.
"""
from typing import List
import os


def generate_pyproject_toml(
    project_name: str,
    database_type: str,
    enable_auth: bool,
    output_path: str
) -> str:
    """
    Generate pyproject.toml file as a static template.
    
    Args:
        project_name: Name of the project
        database_type: "sql" or "mongodb"
        enable_auth: Whether authentication is enabled
        output_path: Full path where the file should be written
        
    Returns:
        The file path where it was written
    """
    # Build dependencies based on database type and auth
    base_deps = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "pydantic-settings",
    ]
    
    if database_type == "sql":
        db_deps = [
            "sqlalchemy",
        ]
    else:  # mongodb
        db_deps = [
            "motor",
            "beanie",
        ]
    
    auth_deps = []
    if enable_auth:
        auth_deps = [
            "python-jose[cryptography]",
            "passlib[bcrypt]",
            "python-multipart",
        ]
    
    all_deps = base_deps + db_deps + auth_deps
    deps_str = ",\n    ".join([f'"{dep}"' for dep in all_deps])
    
    pyproject_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    {deps_str},
]

[tool.setuptools]
packages = ["app"]
'''
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pyproject_content)
    
    return output_path


def generate_env_file(
    database_type: str,
    output_path: str
) -> str:
    """
    Generate .env file as a static template.
    
    Args:
        database_type: "sql" or "mongodb"
        output_path: Full path where the file should be written
        
    Returns:
        The file path where it was written
    """
    if database_type == "sql":
        database_url = "sqlite:///./app.db"
        database_comment = "# For PostgreSQL: postgresql://user:password@localhost:5432/dbname"
    else:  # mongodb
        database_url = "mongodb://localhost:27017"
        database_comment = "# For MongoDB Atlas: mongodb+srv://user:password@cluster.mongodb.net/dbname"
    
    env_content = f'''# Application Configuration
PROJECT_NAME="Your Project Name"
VERSION="0.1.0"

# Database Configuration
DATABASE_URL="{database_url}"
{database_comment}

# Security (if authentication is enabled)
SECRET_KEY="your-secret-key-here-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
'''
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    return output_path

