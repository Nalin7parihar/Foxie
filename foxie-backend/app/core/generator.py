"""
Standard mode code generator - one-shot generation.
Uses Google Gemini with RAG for fast prototyping.
"""
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import time
from jinja2 import Environment, FileSystemLoader
from app.utils.rag import load_style_guide_snippets
from app.core.prompts import MASTER_PROMPT_TEMPLATE
from app.core.models import GeneratedCode, CodeFile
from app.utils.parser import parse_fields, Field
from app.utils.api_key_manager import APIKeyManager
from typing import List, Optional

load_dotenv()


def _generate_static_auth_files(database_type: str) -> List[CodeFile]:
    """
    Generate authentication files statically from Jinja2 templates.
    This avoids LLM generation for auth since it's standardized across applications.
    
    Args:
        database_type: "sql" or "mongodb"
        
    Returns:
        List of CodeFile objects for all auth-related files
    """
    # Setup Jinja2 environment
    template_dir = os.path.join("data", "templates", "auth")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )
    
    # Template context
    context = {"database_type": database_type}
    
    auth_files = []
    
    # 1. security.py
    template = env.get_template("security.py.j2")
    auth_files.append(CodeFile(
        file_path="app/core/security.py",
        content=template.render(**context),
        description="Password hashing and JWT token utilities."
    ))
    
    # 2. user.py model
    template = env.get_template("user_model.py.j2")
    auth_files.append(CodeFile(
        file_path="app/models/user.py",
        content=template.render(**context),
        description=f"User model with authentication support ({database_type.upper()})."
    ))
    
    # 3. schemas/user.py
    template = env.get_template("user_schema.py.j2")
    auth_files.append(CodeFile(
        file_path="app/schemas/user.py",
        content=template.render(**context),
        description="User Pydantic schemas for authentication."
    ))
    
    # 4. crud/user.py
    template = env.get_template("user_crud.py.j2")
    auth_files.append(CodeFile(
        file_path="app/crud/user.py",
        content=template.render(**context),
        description="User CRUD operations with password hashing."
    ))
    
    # 5. endpoints/auth.py
    template = env.get_template("auth_endpoints.py.j2")
    auth_files.append(CodeFile(
        file_path="app/api/endpoints/auth.py",
        content=template.render(**context),
        description="Authentication endpoints (register, login, me)."
    ))
    
    # 6. dependencies/auth_dependency.py
    template = env.get_template("auth_dependency.py.j2")
    auth_files.append(CodeFile(
        file_path="app/dependencies/auth_dependency.py",
        content=template.render(**context),
        description="JWT token validation dependency."
    ))
    
    return auth_files


def _generate_core_crud_files(
    client: genai.Client,
    resource: str,
    fields_str: str,
    project_name: str,
    database_type: str,
    style_guide: str,
    database_type_instructions: str,
    database_specific_instructions: str,
    model_name: str
) -> GeneratedCode:
    """Generate only core CRUD files (no auth)."""
    from app.utils.parser import parse_fields
    
    parsed_fields = parse_fields(fields_str)
    fields_list_str = "\n".join([f"- **{f.name}**: {f.type}" for f in parsed_fields])
    
    # Simplified prompt for core CRUD only (Chinese for token efficiency)
    core_prompt = f"""# 角色 / PERSONA
你是一位专精FastAPI的高级软件工程师。编写简洁、规范、健壮且文档完善的Python代码。

# 任务 / TASK
为名为{project_name}的FastAPI应用生成核心CRUD功能文件（不含认证）。

# 必须生成的文件 / REQUIRED FILES
1. app/core/config.py - 使用STYLE GUIDE中的config.py.example，内容必须完全一致
2. app/database/db_session.py - 数据库类型：{database_type}，使用相应示例
3. app/models/base_model.py - 数据库类型：{database_type}，使用相应示例
4. app/models/{{resource}}.py - 资源模型（{database_type}）
5. app/schemas/{{resource}}.py - 必须包含：{{resource}}Base、{{resource}}Create、{{resource}}Update、{{resource}}（主ORM模式，from_attributes=True）
6. app/crud/{{resource}}.py - 创建CRUD类实例模式：
   class CRUD{{Resource}}:
       def get(self, db: Session, id: int) -> Model | None
       def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Model]
       def create(self, db: Session, obj_in: CreateSchema) -> Model
       def update(self, db: Session, db_obj: Model, obj_in: UpdateSchema) -> Model
       def remove(self, db: Session, id: int) -> Model | None
   {{resource}} = CRUD{{Resource}}()  # 创建实例供端点导入
7. app/api/endpoints/{{resource}}.py - API端点（GET /、GET /{{id}}、POST /、PUT /{{id}}、DELETE /{{id}}）：
   - 导入：from app.crud.{{resource}} import {{resource}} as crud_{{resource}}
   - 端点路径参数使用{{resource}}_id（如user_id、product_id），但调用CRUD时使用id参数名
   - GET /{{{{resource}}_id}}：db_obj = crud_{{resource}}.get(db, id={{resource}}_id)
   - GET /：items = crud_{{resource}}.get_multi(db, skip=skip, limit=limit)
   - POST /：new_obj = crud_{{resource}}.create(db, obj_in=obj_in)
   - PUT /{{{{resource}}_id}}：先get获取对象，再crud_{{resource}}.update(db, db_obj=db_obj, obj_in=obj_in)
   - DELETE /{{{{resource}}_id}}：先get获取对象，再crud_{{resource}}.remove(db, id={{resource}}_id)
8. app/api/router.py - 路由聚合（仅资源路由，无认证路由）
9. app/main.py - 主应用（无认证相关导入，仅包含资源路由）

# 重要约束 / CRITICAL CONSTRAINTS
- CRUD必须使用类实例模式：创建CRUD{{Resource}}类，然后创建实例（{{resource}} = CRUD{{Resource}}()）
- 端点必须导入CRUD实例：from app.crud.{{resource}} import {{resource}} as crud_{{resource}}
- CRUD方法名和签名必须与端点中的调用完全匹配
- 端点必须使用CRUD方法，不能直接操作数据库
- 模式必须包含Update模式（所有字段可选，使用Optional或默认值）
- 端点必须使用正确的响应模式（主ORM模式，from_attributes=True）

# 数据库配置 / DATABASE
{database_specific_instructions}

# 风格指南 / STYLE GUIDE
{style_guide}

# 用户输入 / USER INPUT
- 项目名称：{project_name}
- 资源名称：{resource}
- 字段：
{fields_list_str}

# 输出格式 / OUTPUT
返回JSON对象，符合GeneratedCode Pydantic模式。仅包含上述9个文件。不要生成认证相关文件。"""
    
    print("📦 Generating core CRUD files (9 files)...")
    
    # Retry logic for core generation
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=core_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": GeneratedCode
                }
            )
            print("✅ Core CRUD files generated successfully")
            return response.parsed
        except Exception as e:
            error_str = str(e)
            is_503_error = "503" in error_str or "UNAVAILABLE" in error_str or "overloaded" in error_str.lower()
            
            if is_503_error and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"⚠️  Model overloaded (503). Retrying core generation in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            else:
                raise Exception(f"Error generating core CRUD files: {e}")


def _merge_auth_into_router_and_main(
    all_files: List,
    resource: str
) -> None:
    """Update router.py and main.py to include auth routes."""
    import re
    
    # Find router.py and main.py files
    router_file = None
    main_file = None
    
    for file in all_files:
        if file.file_path == "app/api/router.py":
            router_file = file
        elif file.file_path == "app/main.py":
            main_file = file
    
    if not router_file or not main_file:
        print("⚠️  Warning: Could not find router.py or main.py to merge auth routes")
        return
    
    # Update router.py to include auth router
    router_content = router_file.content
    
    # Check if auth router is already included
    if "from app.api.endpoints import auth" not in router_content:
        # Add auth import
        router_content = re.sub(
            r'(from app\.api\.endpoints import \w+)',
            r'\1, auth',
            router_content,
            count=1
        )
        
        # Add auth router inclusion
        if "api_router.include_router(auth.router" not in router_content:
            # Find the resource router inclusion and add auth after it
            pattern = r'(api_router\.include_router\([^)]+\)\s*)'
            match = re.search(pattern, router_content)
            if match:
                router_content = router_content[:match.end()] + \
                    f'\napi_router.include_router(auth.router, tags=["authentication"])\n' + \
                    router_content[match.end():]
    
    router_file.content = router_content
    
    # Update main.py to include auth dependencies if needed
    main_content = main_file.content
    
    # Check if auth dependency is imported (usually not needed in main.py, but check)
    # Main.py usually just includes the router, which already has auth
    
    main_file.content = main_content
    
    print("🔗 Merged auth routes into router and main files")


def generate_crud_feature(
    resource: str,
    fields_str: str,
    project_name: str,
    api_key: Optional[str] = None,
    database_type: str = "sql",
    enable_auth: bool = False
) -> GeneratedCode:
    """
    Generate a complete CRUD feature. Uses static auth generation when enabled.
    This reduces load on the LLM and avoids rate limits.
    
    Args:
        resource: Name of the resource (e.g., "product", "user")
        fields_str: Comma-separated fields (e.g., "name:str,price:float")
        project_name: Name of the project
        api_key: Optional Google Gemini API key
        database_type: "sql" or "mongodb"
        enable_auth: Whether to generate authentication (User model, auth endpoints)
        
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
    
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Build database-specific instructions (Chinese for token efficiency)
    if database_type == "sql":
        database_type_instructions = "使用SQLAlchemy 2.0，带Mapped[]类型提示和mapped_column()"  # Use SQLAlchemy 2.0 with Mapped[] type hints and mapped_column()
        database_specific_instructions = """
SQL数据库：
# For SQL databases:
- 使用SQLAlchemy 2.0+语法，带`Mapped[]`类型提示
# - Use SQLAlchemy 2.0+ syntax with `Mapped[]` type hints
- 使用`mapped_column()`定义列
# - Use `mapped_column()` for column definitions
- 模型继承自`Base`（DeclarativeBase）
# - Models inherit from `Base` (DeclarativeBase)
- 使用SQLAlchemy的`Session`进行数据库操作
# - Use `Session` from SQLAlchemy for database operations
- 使用`select()`语句或`session.query()`
# - Use `select()` statements or `session.query()`
"""
    else:  # mongodb
        database_type_instructions = "使用MongoDB，配合Beanie ODM或Motor异步驱动"  # Use MongoDB with Beanie ODM or Motor async driver
        database_specific_instructions = """
MongoDB数据库：
# For MongoDB databases:
- 使用Beanie Document语法或Motor异步客户端
# - Use Beanie Document syntax or Motor async client
- 模型继承自`BaseDocument`（Beanie Document）
# - Models inherit from `BaseDocument` (Beanie Document)
- 使用`AsyncIOMotorClient`进行数据库操作
# - Use `AsyncIOMotorClient` for database operations
- 所有数据库操作使用async/await
# - Use async/await for all database operations
- 通过`db.collection_name`访问集合
# - Collections are accessed via `db.collection_name`
"""
    
    # If auth is enabled, generate core CRUD first, then add static auth files
    if enable_auth:
        print("🔄 Generating core CRUD first, then adding static auth files...")
        
        # Step 1: Generate core CRUD files (without auth)
        print(f"📚 Loading core style guide snippets (DB: {database_type})...")
        core_style_guide = load_style_guide_snippets(
            database_type=database_type,
            enable_auth=False  # Load without auth examples for core
        )
        
        print("\n🤖 Step 1/2: Generating core CRUD files (9 files)...")
        core_result = _generate_core_crud_files(
            client=client,
            resource=resource,
            fields_str=fields_str,
            project_name=project_name,
            database_type=database_type,
            style_guide=core_style_guide,
            database_type_instructions=database_type_instructions,
            database_specific_instructions=database_specific_instructions,
            model_name=model_name
        )
        
        all_files = core_result.files
        
        # Step 2: Generate auth files statically (no LLM call)
        print("\n🔐 Step 2/2: Generating authentication files statically (6 files)...")
        auth_files = _generate_static_auth_files(database_type)
        all_files.extend(auth_files)
        
        # Update router.py and main.py to include auth routes
        print("\n🔗 Merging auth routes into router and main files...")
        _merge_auth_into_router_and_main(all_files, resource)
        
        print(f"\n✅ Successfully generated {len(all_files)} files (9 core + 6 auth)")
        return GeneratedCode(files=all_files)
    
    else:
        # No auth: Single call for core CRUD only
        print(f"📚 Loading style guide snippets (DB: {database_type})...")
        style_guide = load_style_guide_snippets(
            database_type=database_type,
            enable_auth=False
        )
        
        print("🤖 Generating core CRUD files (9 files)...")
        return _generate_core_crud_files(
            client=client,
            resource=resource,
            fields_str=fields_str,
            project_name=project_name,
            database_type=database_type,
            style_guide=style_guide,
            database_type_instructions=database_type_instructions,
            database_specific_instructions=database_specific_instructions,
            model_name=model_name
        )
