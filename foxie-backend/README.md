# 🧠 Foxie Backend

FastAPI backend service for the Foxie AI code generator.

This is the AI-powered code generation engine that handles all code generation requests.

For full documentation, see the [main README](../README.md).

## Quick Start

```bash
docker-compose up backend
```

## Configuration

### Environment Variables

- `HOST` - Server host (default: `0.0.0.0`)
- `PORT` - Server port (default: `8000`)
- `GEMINI_MODEL` - Gemini model to use (default: `gemini-2.5-flash`)
- `GENERATION_TEMPERATURE` - Temperature for code generation (default: `0.7`)

### Important Notes

- **No `.env` file needed** - The backend no longer requires `GOOGLE_API_KEY` in environment variables
- **Users provide their own API keys** - The Gemini API key is sent by the CLI in each request (users pay for their own usage)
- **HTTPS encryption** - Render automatically provides HTTPS/TLS, which encrypts all data (including API keys) in transit, preventing interception
- **API keys are not logged** - The backend never logs API keys to prevent exposure

## API Endpoints

- `POST /scaffold` - Hybrid generation (AI for core CRUD + templates for auth)
- `GET /health` - Health check

## Documentation

See the API docs at `http://localhost:8000/docs` when running.
