# 🧠 Foxie Backend

FastAPI backend service for the Foxie AI code generator.

This is the AI-powered code generation engine that handles all code generation requests.

For full documentation, see the [main README](../README.md).

## Quick Start

```bash
docker-compose up backend
```

## Configuration

Set your Google Gemini API key via environment variable:

```bash
export GOOGLE_API_KEY="your-api-key"
```

Or create a `.env` file in this directory with:

```
GOOGLE_API_KEY=your-api-key
```

## API Endpoints

- `POST /scaffold` - Hybrid generation (AI for core CRUD + templates for auth)
- `GET /health` - Health check

## Documentation

See the API docs at `http://localhost:8000/docs` when running.
