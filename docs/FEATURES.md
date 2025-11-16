# 🚀 Foxie Platform - Features Documentation

This document describes the features and capabilities of the Foxie Platform.

---

## ✨ Core Features

### 1. AI-Powered Code Generation

- **Standard Mode**: Fast, one-shot generation using Google Gemini API
- **Single API Call**: Efficient and cost-effective
- **RAG Integration**: Uses Retrieval-Augmented Generation with style guide examples
- **Production-Ready Code**: Generates complete CRUD features with best practices

### 2. Database Support

#### SQL Databases (Default)

- **SQLAlchemy 2.0+** with modern syntax
- Supports PostgreSQL, MySQL, SQLite
- Type hints with `Mapped[]` and `mapped_column()`
- Async-ready with proper session management

#### MongoDB (NoSQL)

- **Beanie ODM** for document models
- **Motor** async driver for direct MongoDB access
- Async/await support for all operations
- Document-based data modeling

### 3. Authentication System

When enabled, generates a complete authentication system:

#### Generated Files

- `app/core/security.py` - Password hashing (bcrypt) and JWT utilities
- `app/models/user.py` - User model with authentication fields
- `app/schemas/user.py` - User schemas (UserCreate, UserResponse, Login, Token)
- `app/crud/user.py` - User CRUD with password hashing
- `app/api/endpoints/auth.py` - Auth endpoints
  - `POST /auth/register` - User registration
  - `POST /auth/login` - User login (returns JWT token)
  - `GET /auth/me` - Get current user info
- `app/dependencies/auth_dependency.py` - JWT token validation

#### Features

- **Password Hashing**: Uses bcrypt via passlib
- **JWT Tokens**: Secure token generation and validation
- **Protected Routes**: Optional route protection for resource endpoints
- **User Management**: Complete user CRUD operations
- **Database Agnostic**: Works with both SQL and MongoDB

### 4. Route Protection

When `protect_routes=True`:

- POST, PUT, DELETE endpoints require authentication
- GET endpoints can be optionally protected
- Uses JWT token validation via `get_current_user` dependency

---

## 📋 Generated File Structure

### Core Files (Always Generated)

- `app/core/config.py` - Application configuration with Pydantic Settings
- `app/database/db_session.py` - Database session management (SQL)
- `app/database/db_session_mongodb.py` - Database session management (MongoDB)
- `app/models/base_model.py` - Base model class (SQL)
- `app/models/base_model_mongodb.py` - Base document class (MongoDB)
- `app/main.py` - FastAPI application entry point

### Resource Files (Generated per Resource)

- `app/models/{resource}.py` - Database model (SQLAlchemy or Beanie)
- `app/schemas/{resource}.py` - Pydantic schemas
- `app/crud/{resource}.py` - CRUD operations
- `app/api/endpoints/{resource}.py` - FastAPI endpoints
- `app/api/router.py` - API router aggregation

### Auth Files (Generated if `enable_auth=True`)

- `app/core/security.py` - Password hashing and JWT utilities
- `app/models/user.py` - User model
- `app/schemas/user.py` - User schemas
- `app/crud/user.py` - User CRUD operations
- `app/api/endpoints/auth.py` - Authentication endpoints
- `app/dependencies/auth_dependency.py` - Auth dependency

---

## 🎯 Usage Examples

### Basic CRUD (SQL, No Auth)

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-app \
  -r product \
  -f "name:str,price:float,stock:int"
```

### CRUD with Authentication (SQL)

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-app \
  -r product \
  -f "name:str,price:float,stock:int" \
  --enable-auth \
  --protect-routes
```

### MongoDB with Authentication

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-app \
  -r product \
  -f "name:str,price:float,stock:int" \
  --database-type mongodb \
  --enable-auth
```

### Interactive Mode

```bash
docker-compose run --rm cli scaffold fastapi-crud
# Will prompt for all options including database type and auth
```

---

## 🔧 Configuration Options

### CLI Options

#### Required

- `--project-name` / `-p`: Project name
- `--resource` / `-r`: Resource name (e.g., "product", "user")
- `--fields` / `-f`: Fields string (e.g., "name:str,price:float")

#### Optional

- `--database-type` / `-d`: Database type (`sql` or `mongodb`, default: `sql`)
- `--enable-auth`: Enable authentication (default: `False`)
- `--protect-routes`: Protect resource routes with auth (requires `--enable-auth`, default: `False`)

---

## 📦 Dependencies

### SQL Projects

- `fastapi`
- `uvicorn[standard]`
- `sqlalchemy`
- `pydantic`
- `pydantic-settings`
- (If auth enabled) `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`

### MongoDB Projects

- `fastapi`
- `uvicorn[standard]`
- `motor` (MongoDB async driver)
- `beanie` (MongoDB ODM)
- `pydantic`
- `pydantic-settings`
- (If auth enabled) `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`

---

## 🎨 Features Highlights

### 1. **Flexible Database Support**

- Choose between SQL (PostgreSQL/MySQL/SQLite) or MongoDB
- Generated code adapts to your database choice
- Modern async support for both

### 2. **Complete Authentication**

- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt
- Protected route support

### 3. **Production-Ready Code**

- Follows FastAPI best practices
- Proper error handling
- Type hints throughout
- Structured project layout

### 4. **RAG-Enhanced Generation**

- Uses example code from knowledge base
- Consistent style and patterns
- Best practices baked in

---

## 🔒 Security Features (When Auth Enabled)

1. **Password Security**

   - Bcrypt hashing
   - Never stores plain passwords
   - Secure password verification

2. **JWT Tokens**

   - HS256 algorithm
   - Configurable expiration
   - Secure token validation

3. **Route Protection**
   - Optional protection for resource endpoints
   - Token-based authentication
   - Proper error handling for unauthorized access

---

## 📚 Generated Code Examples

### SQL Resource Model

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer
from app.models.base_model import Base

class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
```

### MongoDB Resource Model

```python
from beanie import Document
from pydantic import Field
from app.models.base_model_mongodb import BaseDocument

class Product(BaseDocument):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

    class Settings:
        name = "products"
```

### Protected Endpoint Example

```python
from fastapi import Depends, APIRouter
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  # Protected route
):
    # Create product logic
    ...
```

---

## 🚀 Next Steps After Generation

1. **Setup Dependencies**

   ```bash
   uv venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install -e .
   ```

2. **Configure Database**

   - Update `DATABASE_URL` in `.env` file
   - For SQL: `sqlite:///./app.db` or PostgreSQL/MySQL URL
   - For MongoDB: `mongodb://localhost:27017`

3. **Run the Application**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Test the API**
   - Open `http://localhost:8000/docs` for interactive API documentation
   - If auth enabled: Register a user at `/api/v1/auth/register`
   - Login at `/api/v1/auth/login` to get JWT token
   - Use token in Authorization header: `Bearer <token>`

---

## 💡 Tips

1. **For SQL Projects**: Start with SQLite for development, migrate to PostgreSQL for production
2. **For MongoDB Projects**: Use MongoDB Atlas for cloud hosting or install locally
3. **Authentication**: Always enable auth for production applications
4. **Route Protection**: Enable `protect_routes` if your resource should be private
5. **Multiple Resources**: Run the command multiple times with different resources

---

_For more information, see [Project Structure](./PROJECT_STRUCTURE.md) documentation._
