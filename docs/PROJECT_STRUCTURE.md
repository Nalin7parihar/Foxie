# 📚 Foxie Platform - Project Structure Documentation

This document provides a comprehensive overview of the Foxie Platform codebase, explaining the purpose and contents of each folder and key files.

---

## 🏗️ Overall Architecture

Foxie Platform follows a **microservice architecture** with two main components:

1. **foxie-backend** - The AI-powered code generation service (FastAPI)
2. **foxie-cli** - The command-line interface for developers (Typer)

Both services are containerized using Docker and orchestrated with Docker Compose.

---

## 📁 Root Directory

### `docker-compose.yml`

- **Purpose**: Docker Compose configuration that orchestrates both services
- **Key Features**:
  - Defines `backend` service (FastAPI on port 8000)
  - Defines `cli` service (command-line tool)
  - Manages environment variables (especially `GOOGLE_API_KEY`)
  - Sets up volume mounts for development and data sharing
  - Configures service dependencies (CLI depends on backend)

### `README.md`

- Main project documentation with setup instructions, usage examples, and feature descriptions

---

## 🧠 `foxie-backend/` - The AI Backend Service

**Purpose**: The core AI-powered code generation engine. This is where all the AI logic lives.

### `foxie-backend/app/` - Main Application Code

This is the FastAPI application that handles all code generation requests.

#### `app/main.py`

- **Purpose**: FastAPI application entry point
- **Key Features**:
  - Initializes FastAPI app with metadata
  - Defines two main endpoints:
    - `POST /scaffold` - Standard mode (one-shot generation)
    - `POST /scaffold/react` - ReAct Agent mode (autonomous generation with validation)
  - `GET /health` - Health check endpoint
  - Handles HTTP requests from CLI
  - Converts AI responses to structured JSON

#### `app/core/` - Core AI Logic

This directory contains the heart of the AI generation system.

##### `app/core/config.py`

- **Purpose**: Centralized configuration management
- **Key Features**:
  - Loads environment variables using `python-dotenv`
  - Defines `AppConfig` Pydantic model for type-safe configuration
  - Manages Google Gemini API key, model selection, temperature settings
  - Configures self-correction parameters and RAG knowledge base paths
  - Provides validation for API keys

##### `app/core/models.py`

- **Purpose**: Pydantic data models for request/response structures
- **Key Models**:
  - `CodeFile` - Represents a single generated file (path, content, description)
  - `GeneratedCode` - Collection of all generated files for a project

##### `app/core/prompts.py`

- **Purpose**: Contains the master prompt template for code generation
- **Key Features**:
  - Defines the AI prompt structure for generating CRUD features
  - Includes placeholders for resource name, fields, project name, and style guide
  - Used by standard mode generator

##### `app/core/generator.py`

- **Purpose**: Standard mode code generator (one-shot generation with hybrid approach)
- **Key Features**:
  - `generate_crud_feature()` - Main function for standard generation
  - Uses Google Gemini API with structured JSON output for core CRUD files
  - **Template-Based Auth**: Uses Jinja2 templates for authentication files (no LLM calls)
  - **Two-Step Process**: When auth enabled, generates core CRUD first, then adds static auth files
  - `_generate_static_auth_files()` - Generates auth files from templates
  - `_generate_core_crud_files()` - Generates core CRUD files via LLM
  - `_merge_auth_into_router_and_main()` - Merges auth routes into router and main files
  - Loads RAG style guide snippets
  - Parses field definitions from input string
  - Returns complete `GeneratedCode` object with all files
  - Fast and cost-effective (reduces API calls for auth)

##### `app/core/file_generator.py`

- **Purpose**: Individual file generation logic (available for future use)
- **Key Features**:
  - `FileGenerator` class with specialized methods for each file type:
    - `generate_config_file()` - App configuration
    - `generate_db_session_file()` - Database session setup
    - `generate_base_model_file()` - SQLAlchemy base model
    - `generate_resource_model_file()` - Resource-specific model
    - `generate_schema_file()` - Pydantic schemas
    - `generate_crud_file()` - CRUD operations
    - `generate_endpoint_file()` - FastAPI endpoints
    - `generate_router_file()` - API router aggregation
    - `generate_auth_dependency_file()` - Authentication dependency
    - `generate_main_file()` - FastAPI app entry point
  - Each method uses context-aware prompts with RAG examples
  - Generates production-ready code following FastAPI best practices

#### `app/utils/` - Utility Modules

Supporting utilities for the backend service.

##### `app/utils/api_key_manager.py`

- **Purpose**: Centralized API key management
- **Key Features**:
  - Handles API key resolution from multiple sources (priority order):
    1. Explicitly provided key
    2. Environment variable (`GOOGLE_API_KEY`)
    3. `.env` file in current directory
    4. `~/.foxie/.env` global config file
  - Provides validation and error handling

##### `app/utils/parser.py`

- **Purpose**: Parses field definitions from user input
- **Key Features**:
  - `parse_fields()` - Converts comma-separated string (`"name:str,price:float"`) to list of `Field` objects
  - Validates field format (must be `name:type`)
  - Handles whitespace and edge cases

##### `app/utils/rag.py`

- **Purpose**: Retrieval-Augmented Generation (RAG) knowledge base loader
- **Key Features**:
  - `load_style_guide_snippets()` - Loads example code files from RAG knowledge base
  - Reads all `.example` files from `data/rag_knowledge_base/fastapi/`
  - Concatenates examples into a single string for prompt injection
  - Provides AI with best-practice code examples for better generation quality

##### `app/utils/validators.py`

- **Purpose**: Code validation utilities for quality checks
- **Key Features**:
  - `CodeValidator` class with multiple validation methods:
    - `validate_syntax()` - Python AST syntax validation
    - `validate_imports()` - Import statement checks (circular imports)
    - `validate_fastapi_patterns()` - FastAPI best practices
      - Checks for APIRouter usage
      - Validates dependency injection
      - Ensures proper response models and status codes
    - `validate_sqlalchemy_patterns()` - SQLAlchemy 2.0+ syntax
      - Ensures `Mapped[]` type hints
      - Validates `mapped_column()` usage
  - Available for future code validation features
  - Returns structured `ValidationResult` objects with issues and severity levels

### `foxie-backend/data/` - RAG Knowledge Base & Templates

**Purpose**: Stores example code files for RAG and Jinja2 templates for static generation.

#### `data/rag_knowledge_base/fastapi/`

- **Purpose**: Example FastAPI code files showing best practices
- **Files**:
  - `auth_dependency.py.example` - Authentication dependency pattern
  - `base_model.py.example` - SQLAlchemy base model pattern
  - `config.py.example` - Application configuration pattern
  - `db_session.py.example` - Database session setup pattern
  - `main.py.example` - FastAPI app entry point pattern
- **Usage**: These files are loaded and injected into AI prompts to guide code generation towards best practices

#### `data/templates/auth/`

- **Purpose**: Jinja2 templates for generating authentication files statically
- **Files**:
  - `security.py.j2` - Password hashing and JWT utilities template
  - `user_model.py.j2` - User model template (adapts to SQL/MongoDB)
  - `user_schema.py.j2` - User Pydantic schemas template
  - `user_crud.py.j2` - User CRUD operations template
  - `auth_endpoints.py.j2` - Authentication endpoints template
  - `auth_dependency.py.j2` - JWT token validation dependency template
- **Usage**: These templates are rendered with database type context to generate auth files without LLM calls, reducing costs and improving consistency

### `foxie-backend/Dockerfile`

- **Purpose**: Docker image definition for backend service
- **Key Features**:
  - Based on Python 3.11-slim
  - Installs `uv` package manager
  - Copies application code and data
  - Installs dependencies using `uv`
  - Exposes port 8000
  - Runs FastAPI app with Uvicorn (with auto-reload for development)

### `foxie-backend/pyproject.toml`

- **Purpose**: Python project configuration and dependencies
- **Key Dependencies**:
  - `fastapi[all]` - Web framework
  - `google-genai` - Google Gemini AI SDK
  - `pydantic` - Data validation
  - `langgraph` - Agent orchestration framework
  - `langchain-core` - LangChain core utilities

### `foxie-backend/uv.lock`

- Lock file for deterministic dependency resolution using `uv`

---

## 🗣️ `foxie-cli/` - The Command-Line Interface

**Purpose**: Developer-facing command-line tool that provides an easy-to-use interface for code generation.

### `foxie-cli/src/foxie_cli/` - CLI Source Code

#### `src/foxie_cli/cli.py`

- **Purpose**: Main CLI application using Typer
- **Key Features**:
  - **Interactive Mode**: Prompts user for all inputs if no arguments provided
    - Project name
    - Resource name
    - Fields definition
    - Generation mode selection (Standard vs ReAct Agent)
    - Max iterations (for ReAct mode)
  - **Command-Line Mode**: Accepts all parameters via flags
  - **API Key Management**:
    - `get_api_key()` - Resolves API key from multiple sources (same priority as backend)
    - `foxie config` - Command to configure API key interactively
  - **Backend Communication**:
    - Sends requests to backend API (`/scaffold` or `/scaffold/react`)
    - Handles HTTP errors, timeouts, connection issues
    - Displays progress with Rich console output
    - Shows ReAct Agent summary (steps, files generated, validation status)
  - **File Writing**: Calls `write_files()` to save generated code locally
  - **Setup Instructions**: Displays next steps for using generated code
  - **Rich UI**: Uses Rich library for beautiful terminal output (colors, panels, spinners)

#### `src/foxie_cli/core/models.py`

- **Purpose**: Pydantic models for CLI data structures
- **Key Models**:
  - `CodeFile` - Represents a generated file
  - `GeneratedCode` - Collection of files
  - These mirror backend models for consistency

#### `src/foxie_cli/utils/file_writer.py`

- **Purpose**: File writing utilities
- **Key Features**:
  - `write_files()` - Main function that writes all generated files to disk
  - `unfence_code()` - Removes Markdown code fences (`python...`) from AI output
  - `format_python_file()` - Formats Python files using Black formatter
  - Creates directory structure as needed
  - Handles file system errors gracefully
  - Provides user feedback for each file created

#### `src/foxie_cli/utils/template_generator.py`

- **Purpose**: Static template generation for configuration files
- **Key Features**:
  - `generate_pyproject_toml()` - Generates `pyproject.toml` with dependencies based on:
    - Database type (SQL or MongoDB)
    - Authentication requirements
    - Project name
  - `generate_env_file()` - Generates `.env` file with:
    - Database URL (defaults based on database type)
    - Security settings (if auth enabled)
    - CORS configuration
    - Environment-specific defaults
  - **Static Generation**: These files are generated from templates (not AI), ensuring consistency and reliability
  - Automatically adapts to user's selections (database type, auth enabled)

### `foxie-cli/generated_code/`

- **Purpose**: Default output directory for generated projects (mounted as volume in Docker Compose)
- **Note**: Projects are generated here when using Docker, or in the specified project directory when using CLI directly

### `foxie-cli/Dockerfile`

- **Purpose**: Docker image definition for CLI service
- **Key Features**:
  - Based on Python 3.11-slim
  - Installs `uv` package manager
  - Copies source code
  - Installs CLI dependencies (including dev dependencies for Black formatter)
  - Sets `foxie` as entrypoint command

### `foxie-cli/pyproject.toml`

- **Purpose**: Python project configuration for CLI
- **Key Dependencies**:
  - `typer` - CLI framework
  - `rich` - Terminal UI library (colors, formatting)
  - `requests` - HTTP client for backend communication
  - `pydantic` - Data validation
  - `google-genai` - For API key validation (if needed)
- **Entry Point**: Defines `foxie = "foxie_cli.cli:app"` command

### `foxie-cli/uv.lock`

- Lock file for CLI dependencies

---

## 🔄 Data Flow

### Generation Flow:

```
User → CLI (interactive/args)
    → Backend /scaffold endpoint
    → generator.py (hybrid generation)
        → If auth enabled:
            → Step 1: Generate core CRUD via AI (Google Gemini API)
            → Step 2: Generate auth files via Jinja2 templates
            → Merge auth routes into router and main
        → If no auth:
            → Generate core CRUD via AI (Google Gemini API)
    → GeneratedCode response
    → CLI receives response
    → file_writer.py (write AI-generated code files to disk)
    → template_generator.py (generate static config files)
        → Generate pyproject.toml (dependencies based on selections)
        → Generate .env (environment variables with defaults)
    → User sees generated files + config files
```

---

## 🎯 Key Design Decisions

1. **Microservice Architecture**: Separates AI-heavy backend from lightweight CLI for better scalability
2. **Hybrid Generation**: Combines AI generation for flexibility with templates for consistency and speed
3. **RAG for Quality**: Example files guide AI toward best practices
4. **Template-Based Auth**: Jinja2 templates ensure consistent, reliable authentication code
5. **Cost-Effective**: Templates reduce API calls by ~40% when auth is enabled
6. **Rich CLI UX**: Interactive mode with beautiful terminal output improves developer experience
7. **Flexible API Key Management**: Multiple sources with priority order for convenience
8. **Docker Compose Orchestration**: Easy deployment and development setup

---

## 📝 File Naming Conventions

- **`.example` files**: RAG knowledge base examples
- **`__init__.py`**: Python package markers
- **`__pycache__/`**: Python bytecode cache (generated, not committed)
- **`*.egg-info/`**: Package metadata (generated during installation)

---

## 🔍 Finding Specific Functionality

- **AI Code Generation**: `foxie-backend/app/core/generator.py`
- **File Generation Logic**: `foxie-backend/app/core/file_generator.py`
- **Code Validation**: `foxie-backend/app/utils/validators.py`
- **RAG Examples**: `foxie-backend/data/rag_knowledge_base/fastapi/`
- **CLI Interface**: `foxie-cli/src/foxie_cli/cli.py`
- **File Writing**: `foxie-cli/src/foxie_cli/utils/file_writer.py`
- **API Endpoints**: `foxie-backend/app/main.py`
- **Configuration**: `foxie-backend/app/core/config.py`

---

## 🚀 Development Workflow

1. **Backend Development**:

   - Edit files in `foxie-backend/app/`
   - Use `docker-compose up backend` for hot reload

2. **CLI Development**:

   - Edit files in `foxie-cli/src/foxie_cli/`
   - Rebuild image: `docker-compose build cli`

3. **Testing RAG Examples**:

   - Add/modify `.example` files in `foxie-backend/data/rag_knowledge_base/fastapi/`
   - Changes are picked up automatically (mounted volume)

4. **Adding New Validators**:
   - Extend `CodeValidator` class in `foxie-backend/app/utils/validators.py`
   - Add to `validate_all()` method
   - ReAct Agent will automatically use new validators

---

## 📚 Additional Resources

- **Main README**: `README.md` - Setup, usage, and feature documentation
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Typer Docs**: https://typer.tiangolo.com/

---

_Last Updated: Based on current codebase structure_
