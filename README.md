# 🦊 Foxie Platform — AI Code Scaffolding for FastAPI

**Foxie** is an **AI-powered code scaffolding platform** designed to supercharge your **FastAPI** development workflow.  
It automatically generates complete CRUD modules — models, schemas, CRUD logic, endpoints, routers, and more — with a hybrid approach combining AI generation and template-based code.

**✨ Latest Features:** Hybrid generation approach - **template-based authentication** for speed and reliability, combined with AI-powered core CRUD generation!

Powered by **Google Gemini**, Foxie brings intelligent code generation to your fingertips — following best practices for scalable, production-ready FastAPI applications.

---

## 🚀 Generation Approach

Foxie uses a **hybrid generation strategy** for optimal speed, quality, and cost-effectiveness:

| Component          | Method                  | Speed            | Quality            | Benefits                        |
| ------------------ | ----------------------- | ---------------- | ------------------ | ------------------------------- |
| **Core CRUD**      | AI-powered (Gemini)     | ⚡⚡⚡ Fast      | ⭐⭐⭐⭐ Excellent | Flexible, adapts to your needs  |
| **Authentication** | Template-based (Jinja2) | ⚡⚡⚡⚡ Fastest | ⭐⭐⭐⭐⭐ Perfect | Consistent, reliable, cost-free |

**Why Hybrid?**

- ✅ **Faster**: Templates generate auth files instantly (no API calls)
- ✅ **Cheaper**: Reduces LLM API usage by ~40% when auth is enabled
- ✅ **More Reliable**: Templates ensure consistent, tested auth code
- ✅ **Database-Aware**: Templates automatically adapt to SQL or MongoDB
- ✅ **Production-Ready**: Auth code follows security best practices

---

## �🧩 Architecture Overview

Foxie follows a **microservice architecture** for flexibility, maintainability, and scalability — all managed with **Docker Compose**.

### 1. 🧠 `foxie-backend` ("The Kitchen")

The **backend service** handles all AI-related operations.

- Built with **FastAPI**
- Exposes REST APIs to receive scaffolding requests
- Uses **Google Gemini** and **RAG (Retrieval-Augmented Generation)** for structured code generation
- **✨ Main endpoint:**
  - `/scaffold` - Hybrid generation (AI for core CRUD + templates for auth)
- Produces full CRUD modules (models, schemas, endpoints, etc.)

### 2. 🗣️ `foxie-cli` ("The Waiter")

The **command-line interface (CLI)** provides the developer-facing interaction.

- Built with **Typer** (for CLI UX) and **Rich** (for output styling)
- **✨ Interactive mode** - Prompts for all configuration options
- Calls appropriate `foxie-backend` API endpoint
- Writes generated files locally
- Shows generation progress and file summaries
- Outputs setup instructions for the new project

> 💡 This separation ensures the AI-heavy backend can scale independently, while the CLI remains lightweight and portable.

---

## ⚙️ Tech Stack

| Layer                  | Technologies                                                                |
| ---------------------- | --------------------------------------------------------------------------- |
| **Backend**            | FastAPI, Google Generative AI SDK, Pydantic, python-dotenv, Uvicorn, Jinja2 |
| **CLI**                | Typer[rich], Requests, Pydantic                                             |
| **AI Model**           | Google Gemini (via API)                                                     |
| **Templates**          | Jinja2 templates for authentication files                                   |
| **Orchestration**      | Docker, Docker Compose                                                      |
| **Package Management** | [uv](https://github.com/astral-sh/uv)                                       |

---

## 🧰 Prerequisites

Before getting started, ensure you have:

- 🐍 **Python 3.11+** installed
- 🌐 **Backend deployed** (or running locally) - See [Backend Setup](#-backend-setup) below
- 🔑 A **Google Gemini API key** → [Get your API key](https://makersuite.google.com/app/apikey)

---

## � API Key Configuration

Foxie needs a Google Gemini API key to function. You have **multiple options** to provide it:

### Option 1: Interactive Configuration (Recommended)

```bash
foxie config
```

This saves your key to `~/.config/foxie/config.env` for future use.

### Option 2: Environment Variable

Set the `GOOGLE_API_KEY` environment variable:

**Windows (PowerShell):**

```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

**Linux/macOS:**

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### Option 3: Project .env File

Create a `.env` file in your project directory:

```bash
# .env
GOOGLE_API_KEY=your-api-key-here
```

### Option 4: Global Config File

Create `~/.config/foxie/config.env` manually (follows XDG Base Directory specification):

**Windows:**

```powershell
New-Item -Path "$HOME\.config\foxie" -ItemType Directory -Force
Set-Content -Path "$HOME\.config\foxie\config.env" -Value "GOOGLE_API_KEY=your-api-key-here"
```

**Linux/macOS:**

```bash
mkdir -p ~/.config/foxie
echo "GOOGLE_API_KEY=your-api-key-here" > ~/.config/foxie/config.env
```

### Priority Order

Foxie checks for your API key in this order (highest priority first):

1. ✅ `GOOGLE_API_KEY` environment variable
2. ✅ `.env` file in current directory
3. ✅ `~/.config/foxie/config.env` file (standard config location)
4. ❌ Interactive prompt (if none found)

---

## 🖥️ Backend Setup

The Foxie backend can be run in two ways:

### Option 1: Deploy on Render (Recommended for Production)

1. Deploy the `foxie-backend` service on [Render](https://render.com)
2. Set environment variables (if needed):
   - `HOST` (default: `0.0.0.0`)
   - `PORT` (default: `8000`)
   - `GEMINI_MODEL` (default: `gemini-2.5-flash`)
3. Configure your CLI to use the deployed backend URL (see above)

**Note:** The backend doesn't require `GOOGLE_API_KEY` - users provide their own keys via the CLI.

### Option 2: Run Locally with Docker

For local development:

```bash
# Clone the repository
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie

# Start the backend
docker-compose up -d backend

# Set the backend URL for local development
export FOXIE_BACKEND_URL="http://127.0.0.1:8000"
```

See [foxie-backend/README.md](foxie-backend/README.md) for more details.

---

## 🧭 Project Structure

```
Foxie/
├── foxie-backend/          # FastAPI microservice ("Kitchen")
│   ├── app/
│   ├── Dockerfile
│   └── ...
├── foxie-cli/              # Typer CLI ("Waiter")
│   ├── src/foxie_cli/
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── .env
```

---

## 📖 Usage Examples

### Interactive Mode (Recommended)

```bash
# Just run the command and answer the prompts
foxie scaffold fastapi-crud

# The CLI will ask:
# - Project name
# - Resource name
# - Fields
# - Database type (SQL or MongoDB)
# - Enable authentication?
```

### Command-Line Mode

**Standard Mode:**

```bash
foxie scaffold fastapi-crud \
  -p blog-api \
  -r post \
  -f "title:str,content:str,author:str,published:bool"
```

**With Authentication:**

```bash
foxie scaffold fastapi-crud \
  -p ecommerce-api \
  -r product \
  -f "name:str,price:float,stock:int,category:str" \
  -d sql \
  --enable-auth
```

### Generation Process

When you run Foxie, here's what happens:

1. **Core CRUD Generation** (AI-powered):

   - Models, schemas, CRUD operations, endpoints
   - Uses Google Gemini with RAG examples
   - Adapts to your database type (SQL/MongoDB)

2. **Authentication Generation** (if enabled, template-based):

   - User model, auth endpoints, JWT utilities
   - Generated from Jinja2 templates (instant, no API calls)
   - Automatically adapts to your database type

3. **Configuration Files** (static templates):

   - `pyproject.toml` - Project dependencies and configuration
   - `.env` - Environment variables (database URL, secrets, etc.)
   - Generated automatically based on your selections

4. **File Writing**:
   - All files written to your project directory
   - Python files formatted with Black
   - Ready to use!

````

### Multiple Resources

Generate scaffolding for different resources by running the command multiple times:

```bash
# Generate User resource
foxie scaffold fastapi-crud \
  -p my-app \
  -r user \
  -f "username:str,email:str,age:int"

# Generate Product resource
foxie scaffold fastapi-crud \
  -p my-app \
  -r product \
  -f "name:str,price:float,stock:int"
```

---

## 🎯 Features

- 🤖 **AI-Powered Generation** — Leverages Google Gemini for intelligent code scaffolding
- 📝 **Template-Based Auth** — Jinja2 templates for fast, reliable authentication code
- 🚀 **Full CRUD Boilerplate** — Models, schemas, CRUD operations, routers, and endpoints
- 🗄️ **Multi-Database Support** — SQL (PostgreSQL/MySQL/SQLite) and MongoDB
- 🔐 **Complete Authentication** — User model, JWT tokens, protected routes
- 🎨 **Auto-Formatting** — Generated code is automatically formatted with Black
- 🐳 **Dockerized Workflow** — Isolated, reproducible environment with Docker Compose
- 🔌 **Microservice Architecture** — Scalable backend + lightweight CLI
- 📦 **Production-Ready** — Follows FastAPI best practices out of the box
- 💰 **Cost-Effective** — Hybrid approach reduces API costs by ~40% when auth is enabled

## 🛠️ Development

### Running Locally

For local development, you can run both backend and CLI using Docker:

```bash
# Clone the repository
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie

# Start the backend
docker-compose up -d backend

# Run CLI commands
docker-compose run --rm cli scaffold fastapi-crud
```

### Running Tests

```bash
# Backend tests
docker-compose run --rm backend pytest

# CLI tests (from foxie-cli directory)
cd foxie-cli
pytest
```

### Hot Reload Development

For backend development with hot reload:

```bash
docker-compose up backend
```

The backend will automatically reload on code changes.

---

## 🐛 Troubleshooting

### Backend Not Starting

Check if the API key is set correctly:

```bash
docker-compose run --rm backend env | grep GOOGLE_API_KEY
```

### Permission Issues

If you encounter permission issues with generated files:

```bash
sudo chown -R $USER:$USER ./my-generated-project
```

### CLI Connection Errors

Ensure the backend is running:

```bash
docker-compose ps
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Modern, fast web framework
- [Google Gemini API](https://ai.google.dev/) — Powerful AI code generation
- [Typer](https://typer.tiangolo.com/) — CLI framework with great UX
- [Docker](https://www.docker.com/) — Containerization platform
- [LangGraph](https://github.com/langchain-ai/langgraph) — Future agent orchestration

---

## 💬 Support

- 📧 **Email:** nalin7parihar@gmail.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/Nalin7parihar/Foxie/issues)
- 💡 **Discussions:** [GitHub Discussions](https://github.com/Nalin7parihar/Foxie/discussions)

---

<div align="center">

**🦊 Built with ❤️ for Developers Who Code Smarter, Not Harder**

⭐ Star this repo if you find it helpful!

</div>
````
