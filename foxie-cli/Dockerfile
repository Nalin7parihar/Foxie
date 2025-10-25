# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install uv first (can be done before copying code)
RUN pip install uv

# Copy configuration files
COPY pyproject.toml ./
COPY README.md ./
COPY uv.lock ./  

# --- FIX: Copy source code BEFORE installing ---
# This copies the 'src' directory from your host into '/app/src' inside the container
COPY ./src ./src

# --- FIX: Install dependencies AFTER src is copied ---
# Now setuptools (run via pip install -e) can find the './src' directory
RUN uv pip install --system --no-cache  .[dev]

# Set the entrypoint to the 'foxie' command
ENTRYPOINT ["foxie"]

# Default command (optional)
CMD ["--help"]

