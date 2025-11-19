# 🗣️ Foxie CLI

Command-line interface for the Foxie AI code generation platform.

This is the developer-facing CLI tool that provides an easy-to-use interface for code generation.

For full documentation, see the [main README](../README.md).

## Installation

### From PyPI (Recommended)

```bash
pip install foxie-cli
```

### From Source

```bash
git clone https://github.com/foxie-platform/foxie-platform.git
cd foxie-platform/foxie-cli
pip install -e .
```

## Quick Start

```bash
# Interactive mode
foxie scaffold fastapi-crud

# Command-line mode
foxie scaffold fastapi-crud \
  -p my-project \
  -r product \
  -f "name:str,price:float"
```

## Configuration

Foxie requires a Google Gemini API key to function. You can provide it in several ways:

### Option 1: Interactive Configuration (Recommended)

```bash
foxie config
```

This will prompt you to enter your API key and save it to `~/.config/foxie/config.env` for future use.

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

1. `GOOGLE_API_KEY` environment variable
2. `.env` file in current directory
3. `~/.config/foxie/config.env` file (standard config location)
4. Interactive prompt (if none found)

### Get Your API Key

Get your Google Gemini API key from: https://makersuite.google.com/app/apikey

### Backend Configuration

By default, the CLI connects to a backend at `http://127.0.0.1:8000`. If your backend is deployed elsewhere (e.g., on Render), configure the following:

#### Backend URL

Set the `FOXIE_BACKEND_URL` environment variable:

**Windows (PowerShell):**

```powershell
$env:FOXIE_BACKEND_URL="https://your-backend-url.onrender.com"
```

**Linux/macOS:**

```bash
export FOXIE_BACKEND_URL="https://your-backend-url.onrender.com"
```

You can also add the backend URL to your config file (`~/.config/foxie/config.env`):

```bash
# ~/.config/foxie/config.env
FOXIE_BACKEND_URL=https://your-backend-url.onrender.com
GOOGLE_API_KEY=your-gemini-api-key-here
```

**Note:** **API keys are protected by HTTPS** - When using Render, all traffic is encrypted via HTTPS/TLS, preventing interception

## Usage

See the [main documentation](../README.md) for detailed usage instructions.
