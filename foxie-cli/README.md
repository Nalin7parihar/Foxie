# 🗣️ Foxie CLI

Command-line interface for the Foxie AI code generation platform.

This is the developer-facing CLI tool that provides an easy-to-use interface for code generation.

For full documentation, see the [main README](../README.md).

## Installation

```bash
pip install foxie-cli
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

Set your Google Gemini API key:

```bash
foxie config
```

Or set `GOOGLE_API_KEY` environment variable.

## Usage

See the [main documentation](../README.md) for detailed usage instructions.
