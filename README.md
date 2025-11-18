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

- 🐳 **Docker & Docker Compose** installed and running → [Install Docker](https://docs.docker.com/get-docker/)
- 🔑 A **Google Gemini API key** → [Get your API key](https://makersuite.google.com/app/apikey)

---

## � API Key Configuration

Foxie needs a Google Gemini API key to function. You have **multiple options** to provide it:

### Option 1: Interactive Setup (Recommended for first-time users)

When you run Foxie for the first time, it will automatically prompt you for your API key:

```bash
foxie scaffold fastapi-crud
```

The CLI will:

- Prompt you to enter your API key (hidden input for security)
- Offer to save it to `~/.foxie/.env` for future use
- Remember it for all future Foxie commands

### Option 2: Pre-configure with CLI Command

Set up your API key before using Foxie:

```bash
foxie config
```

This saves your key to `~/.foxie/.env` so you never have to enter it again.

### Option 3: Environment Variable

Set the `GOOGLE_API_KEY` environment variable:

**Windows (PowerShell):**

```powershell
$env:GOOGLE_API_KEY="AIzaYourActualApiKeyGoesHere"
```

**Linux/macOS:**

```bash
export GOOGLE_API_KEY="AIzaYourActualApiKeyGoesHere"
```

### Option 4: Project .env File

Create a `.env` file in your project directory:

```bash
# .env
GOOGLE_API_KEY=AIzaYourActualApiKeyGoesHere
```

### Option 5: Global Config File

Create `~/.foxie/.env` manually:

**Windows:**

```powershell
New-Item -Path "$HOME\.foxie" -ItemType Directory -Force
Set-Content -Path "$HOME\.foxie\.env" -Value "GOOGLE_API_KEY=AIzaYourActualApiKeyGoesHere"
```

**Linux/macOS:**

```bash
mkdir -p ~/.foxie
echo "GOOGLE_API_KEY=AIzaYourActualApiKeyGoesHere" > ~/.foxie/.env
```

### Priority Order

Foxie checks for your API key in this order (highest priority first):

1. ✅ Explicitly passed to CLI/API
2. ✅ `GOOGLE_API_KEY` environment variable
3. ✅ `.env` file in current directory
4. ✅ `~/.foxie/.env` global config file
5. ❌ Prompts you to enter it

---

## 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie
```

### 2. Configure Your API Key

Choose one of the options above to set your Google Gemini API key.

````

⚠️ **Important:** This key will be securely passed into the backend container via Docker Compose.

### 3. Build Docker Images

```bash
docker-compose build
````

### 4. Run the Backend Service

Start the backend in detached mode:

```bash
docker-compose up -d backend
```

Check logs if needed:

```bash
docker-compose logs -f backend
```

### 5. Run the CLI Command

**🎯 Interactive Mode (Recommended):**

Simply run without options and the CLI will guide you:

```bash
docker-compose run --rm cli scaffold fastapi-crud
```

The CLI will interactively prompt for:

- 📦 Project name
- 🏷️ Resource name
- 📝 Fields definition
- 🗄️ Database type (SQL or MongoDB)
- 🔐 Enable authentication?

**⚡ Command-Line Mode (for automation):**

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-gadget-app \
  -r widget \
  -f "name:str,color:str,weight:float" \
  -d sql \
  --enable-auth
```

This will:

- ✅ Send the command to the AI backend
- ✅ Generate complete CRUD boilerplate for your FastAPI project
- ✅ Use templates for authentication files (fast and reliable)
- ✅ Save the files to your local directory
- ✅ Print setup and usage instructions for your new project

> 💡 **Tip:** Use `--enable-auth` to add a complete authentication system with JWT tokens!

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
docker-compose run --rm cli scaffold fastapi-crud

# The CLI will ask:
# - Project name
# - Resource name
# - Fields
# - Max iterations (if agentic enabled)
```

### Command-Line Mode

**Standard Mode (Fast):**

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p blog-api \
  -r post \
  -f "title:str,content:str,author:str,published:bool"
```

**With Authentication:**

```bash
docker-compose run --rm cli scaffold fastapi-crud \
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
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-app \
  -r user \
  -f "username:str,email:str,age:int"

# Generate Product resource
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-app \
  -r product \
  -f "name:str,price:float,stock:int"
````

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

### Running Tests

```bash
# Backend tests
docker-compose run --rm backend pytest

# CLI tests
docker-compose run --rm cli pytest
```

### Hot Reload Development

For development with hot reload:

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
