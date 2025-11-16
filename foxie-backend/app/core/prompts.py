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

# 1. File Structure: Generate ALL required files. Assume the base structure is `app/`.
#    Core components go in `app/core/`, database setup in `app/database/`,
#    models in `app/models/`, schemas in `app/schemas/`, CRUD logic in `app/crud/`,
#    API endpoints in `app/api/endpoints/`, and dependencies in `app/dependencies/`.

# 2. Configuration (`app/core/config.py`): 
#    - You MUST create an `app/core/config.py` file.
#    - The content of this file MUST be EXACTLY the content provided in the
#      `config.py.example` snippet from the STYLE GUIDE section. Do not modify it.

# 3. Database Session (`app/database/db_session.py`): 
#    - Database type is: {database_type}
#    - For SQL: Use `db_session.py.example` with SQLAlchemy
#    - For MongoDB: Use `db_session_mongodb.py.example` with Motor/Beanie
#    - The content MUST match the appropriate example from STYLE GUIDE.

# 4. Base Model (`app/models/base_model.py`):
#    - Database type is: {database_type}
#    - For SQL: Use `base_model.py.example` with SQLAlchemy DeclarativeBase
#    - For MongoDB: Use `base_model_mongodb.py.example` with Beanie Document
#    - The content MUST match the appropriate example from STYLE GUIDE.

# 5. Authentication (if enable_auth={enable_auth}):
#    - If enable_auth is True, you MUST generate ALL auth-related files:
#      a) `app/core/security.py` - Password hashing and JWT utilities (use security.py.example)
#      b) `app/models/user.py` - User model with password field (use user_model.py.example, adapt for {database_type})
#      c) `app/schemas/user.py` - User schemas (UserCreate, UserResponse, Login, Token)
#      d) `app/crud/user.py` - User CRUD operations with password hashing
#      e) `app/api/endpoints/auth.py` - Auth endpoints (use auth_endpoints.py.example, adapt for {database_type})
#      f) `app/dependencies/auth_dependency.py` - Auth dependency (use auth_dependency.py.example)
#    - User model MUST include: username, email, hashed_password, is_active, is_superuser
#    - Auth endpoints MUST include: POST /auth/register, POST /auth/login, GET /auth/me
#    - Login MUST return JWT token using create_access_token from security.py
#    - Registration MUST hash password using get_password_hash from security.py

# 6. Resource Model (`app/models/{{resource}}.py`): 
#    - Database type is: {database_type}
#    - For SQL: Use SQLAlchemy 2.0 syntax (`Mapped`, `mapped_column`)
#      - Model MUST inherit from 'Base' class defined in `app/models/base_model.py`
#      - Map fields: str → String, int → Integer, float → Float, bool → Boolean
#    - For MongoDB: Use Beanie Document syntax
#      - Model MUST inherit from 'BaseDocument' class defined in `app/models/base_model_mongodb.py`
#      - Use Pydantic Field for validation
#    - Map user-provided fields to appropriate types for the database system.

# 7. Pydantic Schemas (`app/schemas/{{resource}}.py`): 
#    - Create the specific schema file (e.g., `app/schemas/product.py`).
#    - Create `...Base`, `...Create`, `...Update`, and the main ORM-enabled schema.
#    - For MongoDB: Schemas work the same way with Pydantic

# 8. CRUD Logic (`app/crud/{{resource}}.py`): 
#    - Database type is: {database_type}
#    - For SQL: Functions take `db: Session` from SQLAlchemy
#      - Use `select()` with `session.execute()` or `session.query()`
#      - Implement: get, get_multi, create, update, remove
#    - For MongoDB: Functions take `db: AsyncIOMotorClient` or use Beanie Document methods
#      - Use `db.collection_name.find_one()`, `find()`, `insert_one()`, etc.
#      - Or use Beanie: `DocumentClass.find_one()`, `DocumentClass.find()`, `document.insert()`
#    - If enable_auth=True: Also create `app/crud/user.py` with password hashing in create function

# 9. API Endpoint (`app/api/endpoints/{{resource}}.py`): 
#    - Create the specific endpoint file (e.g., `app/api/endpoints/product.py`).
#    - Create an `APIRouter` (e.g., `router = APIRouter()`).
#    - Implement the 5 standard CRUD endpoints: GET /, GET /{{id}}, POST /, PUT /{{id}}, DELETE /{{id}}
#    - Database type is: {database_type}
#    - For SQL: Inject `db: Session = Depends(get_db)` from `app.database.db_session`
#    - For MongoDB: Inject `db: AsyncIOMotorClient = Depends(get_db)` or use async Beanie methods
#    - If enable_auth=True and protect_routes={protect_routes}:
#      - Protect POST, PUT, DELETE endpoints: `user: User = Depends(get_current_user)`
#      - Optionally protect GET / (list) endpoint
#      - GET /{{id}} can be public or protected based on use case
#    - Use correct status codes: 200 for GET, 201 for POST, 204 for DELETE, 404 for not found

# 10. Main API Router (`app/api/router.py`): 
#     - You MUST create `app/api/router.py`.
#     - Import the specific resource router (e.g., `from app.api.endpoints import product`).
#     - If enable_auth=True: Import auth router (e.g., `from app.api.endpoints import auth`)
#     - Create `api_router = APIRouter(prefix="/api/v1")` and include routers:
#       - Resource router: `api_router.include_router(product.router, prefix="/products", tags=["products"])`
#       - Auth router (if enabled): `api_router.include_router(auth.router, tags=["authentication"])`

# 11. Main Application (`app/main.py`): 
#     - You MUST create `app/main.py`.
#     - Use the `main.py.example` from the STYLE GUIDE as a base.
#     - If MongoDB: Add startup/shutdown events for `init_db()` and `close_db()`
#     - Import and include the api_router from `app.api.router`

# 12. Imports: Ensure all imports are absolute (e.g., `from app.core.config import settings`).

# 13. Indentation & Formatting: 
#     - You MUST use 4 spaces for indentation.
#     - All generated Python code must be syntactically correct and perfectly formatted.
#     - Wrap all code blocks in ```python ... ``` fences.

# DATABASE & AUTH CONFIGURATION

- **Database Type:** {database_type}
- **Enable Authentication:** {enable_auth}
- **Protect Routes:** {protect_routes}

{database_specific_instructions}

{auth_specific_instructions}

# STYLE GUIDE & BEST PRACTICES
# You MUST use the following code snippets as your definitive style guide.
# Your generated code must be 100% consistent with these examples,
# especially for things like database sessions or dependencies.

{style_guide}

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
            "description": "SQLAlchemy/Beanie model for the product resource."
        }},
        {{
            "file_path": "app/schemas/product.py",
            "content": "# The full python code for the schema file...",
            "description": "Pydantic schemas for product creation, update, and reading."
        }}
    ]
}}
```

"""