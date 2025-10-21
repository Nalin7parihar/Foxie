# 🦊 Foxie

**AI-Powered FastAPI Project Scaffolder**

> ⚠️ **WORK IN PROGRESS** - This project is currently under active development. Features may be incomplete, unstable, or subject to change.

Foxie is a command-line tool that helps you quickly scaffold FastAPI projects with full CRUD operations using the power of Google's Generative AI. Generate complete FastAPI applications with models, schemas, routers, and database integration in seconds!

## ✨ Features

- 🚀 **FastAPI CRUD Generation**: Automatically generate complete CRUD endpoints
- 🤖 **AI-Powered**: Uses Google Gemini AI to generate high-quality, production-ready code
- 📦 **Complete Project Structure**: Generates models, schemas, routers, and database setup
- 🛠️ **CLI-First**: Simple command-line interface for quick project generation
- 🔧 **Customizable**: Specify your own models and fields
- 📚 **Well-Structured**: Follows FastAPI best practices and conventions

## 📋 Prerequisites

- Python 3.11+
- Google AI API key (for Gemini AI)
- uv package manager (recommended)

## 🚀 Installation

> **Note**: As this is a work in progress, installation may require additional setup steps not yet documented.

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie

# Install dependencies
uv sync

# Install the CLI tool
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie

# Install dependencies
pip install -r requirements.txt

# Install the CLI tool
pip install -e .
```

## ⚙️ Configuration

1. **Get a Google AI API Key**:

   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. **Set up environment variables**:
   ```bash
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

## 🎯 Usage

> **Warning**: The scaffolding functionality is still under development. Generated code may be incomplete or require manual fixes.

### Basic Commands

```bash
# Greet command (fully functional)
foxie greet "Your Name"

# Get help
foxie --help
```

### Scaffold a FastAPI CRUD Application

> **Note**: This feature is currently in development and may not produce complete, runnable code.

```bash
foxie scaffold fastapi-crud \
  --project-name "my-awesome-api" \
  --resource "product" \
  --fields "name:str,price:float,description:str,is_available:bool"
```

### Examples

#### Create a Product Management API

```bash
foxie scaffold fastapi-crud \
  --project-name "product-api" \
  --resource "product" \
  --fields "name:str,price:float,description:str,category:str,in_stock:bool"
```

#### Create a User Management System

```bash
foxie scaffold fastapi-crud \
  --project-name "user-management" \
  --resource "user" \
  --fields "username:str,email:str,first_name:str,last_name:str,is_active:bool"
```

#### Create a Blog API

```bash
foxie scaffold fastapi-crud \
  --project-name "blog-api" \
  --resource "post" \
  --fields "title:str,content:str,author:str,published:bool,created_at:datetime"
```

## 📁 Generated Project Structure

When you run the scaffold command, Foxie generates a complete FastAPI project with:

```
generated_projects/
└── your-project-name/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── product.py
    │   ├── schemas/
    │   │   ├── __init__.py
    │   │   └── product.py
    │   ├── routers/
    │   │   ├── __init__.py
    │   │   └── product.py
    │   └── database.py
    ├── requirements.txt
    ├── README.md
    └── .env.example
```

## 🔧 Field Types

Foxie supports the following field types:

- `str` - String/Text fields
- `int` - Integer numbers
- `float` - Decimal numbers
- `bool` - Boolean values (true/false)
- `datetime` - Date and time fields
- `date` - Date fields only

## 🤖 AI-Powered Code Generation

Foxie uses Google's Gemini AI to generate:

- **SQLAlchemy Models**: Properly defined database models with relationships
- **Pydantic Schemas**: Request/response schemas with validation
- **FastAPI Routers**: Complete CRUD endpoints with error handling
- **Database Configuration**: SQLite/PostgreSQL setup with connection pooling
- **Documentation**: Auto-generated API documentation

## 🛠️ Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=foxie_cli
```

### Code Quality

```bash
# Format code
uv run black foxie_cli/

# Lint code
uv run flake8 foxie_cli/

# Type checking
uv run mypy foxie_cli/
```

## 📚 API Documentation

Generated FastAPI applications include automatic API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚧 Development Status

This project is currently in **active development**. Here's what's implemented and what's planned:

### ✅ Completed Features

- Basic CLI structure with Typer
- Google Gemini AI integration
- Field parsing and validation
- Project scaffolding framework

### 🔄 In Progress

- CRUD code generation
- File writing system
- Database model generation
- API endpoint creation

### 📋 Planned Features

- Multiple database support (PostgreSQL, MySQL, SQLite)
- Authentication system generation
- Testing framework integration
- Docker containerization
- CI/CD pipeline templates
- Advanced AI prompts for better code quality

## 🐛 Known Issues

- Code generation may produce incomplete or non-functional code
- Limited error handling in some areas
- Documentation generation is basic
- Testing coverage is minimal

## 🤝 Contributing

We welcome contributions! Since this is a work in progress, there are many areas where help is needed:

1. **Code Generation**: Improve AI prompts for better code quality
2. **Testing**: Add comprehensive test coverage
3. **Documentation**: Create better examples and guides
4. **Features**: Implement planned features listed above

Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The modern Python web framework
- [Google Gemini AI](https://ai.google.dev/) - For powering intelligent code generation
- [Typer](https://typer.tiangolo.com/) - For the beautiful CLI interface
- [SQLAlchemy](https://www.sqlalchemy.org/) - For database operations

## 📞 Support & Feedback

Since this is a work in progress, your feedback is crucial!

- 🐛 **Report Issues**: [GitHub Issues](https://github.com/Nalin7parihar/Foxie/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Nalin7parihar/Foxie/discussions)
- 📧 **Email**: nalin7parihar@gmail.com

### Getting Help

If you encounter issues:

1. Check the [Development Status](#-development-status) section above
2. Look at the [Known Issues](#-known-issues) section
3. Search existing [GitHub Issues](https://github.com/Nalin7parihar/Foxie/issues)
4. Create a new issue with detailed information about your problem

---

**Made with ❤️ and AI by Nalin Parihar**
