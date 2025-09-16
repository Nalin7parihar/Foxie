# Foxie 🦊

![Status](https://img.shields.io/badge/status-under%20construction-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Powered by](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blueviolet)

**Foxie** is your smart, AI-powered command-line assistant that automatically generates high-quality docstrings for your code, saving you time and effort.

---

## 🚧 Under Construction 🚧

**Please Note:** Foxie is currently in the early stages of development. The core functionality is working, but it is considered an alpha project. Features may change, and the backend service is not yet implemented.

## The Problem

Writing and maintaining good documentation is crucial, but it's often a tedious and time-consuming task that gets pushed aside. Foxie aims to solve this by automating the process, ensuring your code is always well-documented and easy to understand.

## Features

- **AI-Powered Docstrings:** Leverages Google's Gemini models to generate meaningful and context-aware documentation.
- **Simple CLI:** A clean and straightforward command-line interface for easy use.
- **Python Support:** Currently focused on generating Google-style docstrings for Python files.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/Nalin7parihar/Foxie.git](https://github.com/Nalin7parihar/Foxie.git)
    cd foxie
    ```

2.  **Create a virtual environment and install dependencies:**
    (This project uses `uv`, but you can use `pip` as well).
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    uv pip install -r requirements.txt
    ```

## Configuration

Foxie requires a Google Gemini API key to function.

1.  **Create a `.env` file:**
    Copy the example file to create your own local environment file.

    ```bash
    cp .env.example .env
    ```

2.  **Add your API key:**
    Open the newly created `.env` file and paste your Google API key.
    ```
    # .env
    GOOGLE_API_KEY="AIzaSy..."
    ```

## Usage

To generate a docstring for a Python file, simply run the script and pass the path to your file as an argument.

```bash
python foxie_cli.py path/to/your/file.py
```
