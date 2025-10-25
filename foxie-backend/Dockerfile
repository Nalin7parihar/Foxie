# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install uv (faster than pip)
RUN pip install uv

# Copy configuration and README first
COPY pyproject.toml ./
COPY README.md ./  
COPY uv.lock ./

# --- FIX: Copy source code and data BEFORE installing ---
COPY ./app ./app
COPY ./data ./data

# --- FIX: Install dependencies AFTER code is copied ---
# Now setuptools (run via pip install -e) can find the 'app' directory
RUN uv pip install --system --no-cache  .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]

