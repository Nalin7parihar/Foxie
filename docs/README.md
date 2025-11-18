# 📚 Foxie Platform Documentation

Welcome to the Foxie Platform documentation! This directory contains comprehensive documentation about the project structure, architecture, and functionality.

## 📖 Available Documentation

### [Project Structure](./PROJECT_STRUCTURE.md)

Comprehensive guide explaining:

- Overall architecture and design decisions
- Purpose and contents of each folder
- Key files and their responsibilities
- Data flow between components
- Development workflow

### [Features](./FEATURES.md)

Detailed feature documentation:

- Core features and capabilities
- Database support (SQL & MongoDB)
- Authentication system
- Configuration options
- Usage examples

### [Next Steps](./NEXT_STEPS.md)

Future plans and roadmap:

- Short-term improvements (1-2 months)
- Medium-term enhancements (3-6 months)
- Long-term vision (6+ months)
- Technical debt and improvements
- Implementation phases

## 🎯 Quick Navigation

### For New Developers

1. Start with the [main README](../README.md) for setup and quick start
2. Read [Project Structure](./PROJECT_STRUCTURE.md) to understand the codebase
3. Explore the codebase using the file structure guide

### For Contributors

- Review [Project Structure](./PROJECT_STRUCTURE.md) to understand design decisions
- Check the "Finding Specific Functionality" section for quick navigation
- Refer to "Development Workflow" for development practices

## 🔍 Documentation Guide

### Understanding the Architecture

- **Backend (`foxie-backend/`)**: Contains all AI logic, FastAPI endpoints, and code generation
- **CLI (`foxie-cli/`)**: Developer-facing command-line interface
- **Docker Compose**: Orchestrates both services with proper networking and volumes

### Key Concepts

- **Standard Mode**: Fast, one-shot code generation
- **ReAct Agent Mode**: Autonomous generation with validation and self-correction
- **RAG (Retrieval-Augmented Generation)**: Uses example files to guide AI generation
- **LangGraph**: State machine for agent orchestration

## 📝 Contributing to Documentation

When adding new features or making significant changes:

1. Update relevant sections in [Project Structure](./PROJECT_STRUCTURE.md)
2. Keep documentation in sync with code changes
3. Add examples where helpful

---

_For questions or improvements to this documentation, please open an issue or pull request._
