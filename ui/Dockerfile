FROM python:3.12.0

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    PATH="/root/.local/bin:$PATH"

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set work directory
WORKDIR .

# Copy the project files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root --no-dev

# Copy application source code
COPY . .

# Expose port
EXPOSE 3000

# Command to run the FastAPI app
CMD ["poetry", "run", "streamlit", "run", "main.py"]
