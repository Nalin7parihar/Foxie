# This is a template for our master prompt.
# We will format it with the user's resource and fields.

# Note the detailed instructions, the persona, the rules, and the output format specification.
# This level of detail is necessary to get reliable results.

MASTER_PROMPT_TEMPLATE = """
# PERSONA

You are an expert senior software engineer specializing in FastAPI. You write clean, idiomatic, robust, and well-documented Python code that adheres to modern best practices.

# TASK

Your task is to generate a complete and interconnected set of files for a new CRUD (Create, Read, Update, Delete) feature in a FastAPI application having name as {project_name}. You must follow all the rules and constraints provided.

# RULES & CONSTRAINTS

1.  **File Structure:** Generate all required files for the feature. The standard structure is: `models`, `schemas`, `crud`, and `api/endpoints`.
2.  **SQLAlchemy Model (`models.py`):**
    - Use `SQLAlchemy` and assume a standard `Base` declarative base is available.
    - Create a model class (e.g., `Product`) that inherits from `Base`.
    - Include an `id` column as an integer primary key.
    - Map the user-provided fields to the correct `SQLAlchemy` column types.
3.  **Pydantic Schemas (`schemas.py`):**
    - Create a `...Base` schema with the common fields.
    - Create a `...Create` schema inheriting from `...Base`.
    - Create a `...Update` schema inheriting from `...Base` where all fields are optional.
    - Create a main schema (e.g., `Product`) inheriting from `...Base` that includes the `id` and is configured for ORM mode.
4.  **CRUD Logic (`crud.py`):**
    - Implement the five core CRUD functions: `get`, `get_multi`, `create`, `update`, `remove`.
    - All functions must take a `db: Session` as an argument.
    - Use the correct models and schemas. Type hint everything.
5.  **API Router (`api/endpoints/...py`):**
    - Create an `APIRouter`.
    - Implement the five standard CRUD endpoints: `GET /`, `GET /{{id}}`, `POST /`, `PUT /{{id}}`, `DELETE /{{id}}`.
    - Use the correct status codes for each operation (e.g., 201 for POST).
    - Handle `HTTPException` for not-found cases (404).
    - Inject the database session using `Depends`.
6.  **Imports:** Ensure all imports between the generated files are correct and absolute (e.g., `from app.models.product import     Product`).
7.   Main Application (app/main.py)
    You MUST create an 'app/main.py' file.
    You MUST use the 'main.py.example' from the style guide *exactly*. Do not modify it.


# 8. Main API Router (app/api/router.py)
# You MUST create a new file 'app/api/router.py'.
# This file must import the {resource} router (e.g., from 'app.api.endpoints.user')
# and include it in a new 'api_router' APIRouter.
# Example for a 'user' resource:
# from fastapi import APIRouter
# from app.api.endpoints import user
#
# api_router = APIRouter()
# api_router.include_router(user.router, prefix="/users", tags=["users"])

# 9. Indentation & Formatting:
# You MUST use 4 spaces for indentation.
# All generated Python code must be syntactically correct and perfectly formatted.
# Wrap all code blocks in ```python ... ``` fences.

# STYLE GUIDE & BEST PRACTICES
# You MUST use the following code snippets as your definitive style guide.
# Your generated code must be 100% consistent with these examples,
# especially for things like database sessions or dependencies.

{style_guide}  # <--- ADD THIS PLACEHOLDER

# USER INPUT

You will generate a feature for the following resource:
- **Project Name:** `{project_name}`
- **Resource Name:** `{resource}`
- **Fields:**
{fields_list}

# REQUIRED OUTPUT FORMAT

You MUST respond with a JSON object that strictly adheres to the `GeneratedCode` Pydantic schema provided. Do not add any introductory text, concluding remarks, or any other content outside of the JSON structure.

Example JSON structure:
```json
{{
    "files": [
        {{
            "file_path": "app/models/product.py",
            "content": "# The full python code for the model file...",
            "description": "SQLAlchemy model for the product resource."
        }},
        {{
            "file_path": "app/schemas/product.py",
            "content": "# The full python code for the schema file...",
            "description": "Pydantic schemas for product creation, update, and reading."
        }}
    ]
}}

"""