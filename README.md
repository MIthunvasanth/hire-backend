# Hire Backend

AI-powered career development and recruitment platform backend API.

## Setup

```bash
# Install dependencies with uv
uv sync

# Run the application
uv run python app/main.py
```

## Stack

- **FastAPI**: REST API framework
- **Motor**: Async MongoDB driver
- **Redis**: Caching
- **Pydantic**: Data validation

## Modules

- `auth/`: Authentication and user management
- `api/`: REST API endpoints
- `ai_engines/`: AI-powered features (recommendation, gap analysis, etc.)
- `core/`: Configuration and database setup
