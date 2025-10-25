# 🦊 Foxie Platform — AI Code Scaffolding Microservice

**Foxie** is an **AI-powered code scaffolding platform** designed to supercharge your **FastAPI** development workflow.  
It automatically generates complete CRUD modules — models, schemas, CRUD logic, endpoints, routers, and more — based on simple high-level user input.

Powered by **Google Gemini**, Foxie brings intelligent code generation to your fingertips — following best practices for scalable, production-ready FastAPI applications.

---

## 🧩 Architecture Overview

Foxie follows a **microservice architecture** for flexibility, maintainability, and scalability — all managed with **Docker Compose**.

### 1. 🧠 `foxie-backend` ("The Kitchen")

The **backend service** handles all AI-related operations.

- Built with **FastAPI**
- Exposes REST APIs to receive scaffolding requests
- Uses **Google Gemini** and **RAG (Retrieval-Augmented Generation)** for structured code generation
- Produces full CRUD modules (models, schemas, endpoints, etc.)
- (🔮 _Future_: Integration with **LangGraph** for self-correcting agents)

### 2. 🗣️ `foxie-cli` ("The Waiter")

The **command-line interface (CLI)** provides the developer-facing interaction.

- Built with **Typer** (for CLI UX) and **Rich** (for output styling)
- Parses commands like `scaffold fastapi-crud ...`
- Calls `foxie-backend` APIs
- Writes generated files locally, applies formatting with **Black**
- Outputs setup instructions for the new project

> 💡 This separation ensures the AI-heavy backend can scale independently, while the CLI remains lightweight and portable.

---

## ⚙️ Tech Stack

| Layer                  | Technologies                                                        |
| ---------------------- | ------------------------------------------------------------------- |
| **Backend**            | FastAPI, Google Generative AI SDK, Pydantic, python-dotenv, Uvicorn |
| **CLI**                | Typer[rich], Requests, Pydantic                                     |
| **AI Model**           | Google Gemini (via API)                                             |
| **Orchestration**      | Docker, Docker Compose                                              |
| **Package Management** | [uv](https://github.com/astral-sh/uv)                               |
| **(Planned)**          | LangGraph, Celery, Redis                                            |

---

## 🧰 Prerequisites

Before getting started, ensure you have:

- 🐳 **Docker & Docker Compose** installed and running → [Install Docker](https://docs.docker.com/get-docker/)
- 🔑 A **Google Gemini API key** → [Get your API key](https://aistudio.google.com/app/apikey)

---

## 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Nalin7parihar/Foxie.git
cd Foxie
```

### 2. Create Environment File

Create a `.env` file in the root directory:

```bash
# Foxie-Platform/.env
GOOGLE_API_KEY=AIzaYourActualApiKeyGoesHere
```

⚠️ **Important:** This key will be securely passed into the backend container via Docker Compose.

### 3. Build Docker Images

```bash
docker-compose build
```

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

Use the CLI service to scaffold a FastAPI CRUD project.

**Example:** To scaffold a `widget` resource inside a project called `my-gadget-app`:

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p my-gadget-app \
  -r widget \
  -f "name:str,color:str,weight:float"
```

This will:

- ✅ Send the command to the AI backend
- ✅ Generate complete CRUD boilerplate for your FastAPI project
- ✅ Save the files to your local directory
- ✅ Automatically format the code with **black**
- ✅ Print setup and usage instructions for your new project

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

### Basic CRUD Scaffolding

```bash
docker-compose run --rm cli scaffold fastapi-crud \
  -p blog-api \
  -r post \
  -f "title:str,content:str,published:bool"
```

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
```

---

## 🎯 Features

- 🤖 **AI-Powered Generation** — Leverages Google Gemini for intelligent code scaffolding
- 🚀 **Full CRUD Boilerplate** — Models, schemas, CRUD operations, routers, and endpoints
- 🎨 **Auto-Formatting** — Generated code is automatically formatted with Black
- 🐳 **Dockerized Workflow** — Isolated, reproducible environment with Docker Compose
- 🔌 **Microservice Architecture** — Scalable backend + lightweight CLI
- 📦 **Production-Ready** — Follows FastAPI best practices out of the box

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
