# Higgsfield API

Production-grade FastAPI wrapper for Higgsfield's multimodal generation APIs

## Quick Start

### 1. Setup
```bash
# Copy .env file (Higgsfield credentials already included!)
cp .env.example .env

# Install dependencies
pip install -e ".[dev]"
```

### 2. Run
```bash
make run
# OR: uvicorn app.main:app --reload
```

Server starts at: http://localhost:8000

### 3. Test

**Swagger UI (Interactive API Docs):** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

**Test with curl:**
```bash
# Health check
curl http://localhost:8000/health

# Generate image (Text-to-Image)
curl -X POST http://localhost:8000/v1/t2i/nano-banana \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "a monkey", "aspect_ratio": "1:1", "batch_size": 1}'
```

**Run automated tests:**
```bash
make test
```

---

## Features

- **Production-Ready**: Full type safety, comprehensive error handling, structured logging
- **Retry Logic**: Exponential backoff with jitter for all upstream API calls
- **Observability**: Structured JSON logging with request IDs and duration tracking
- **Docker Support**: Multi-stage builds for development and production
- **Well Tested**: Comprehensive integration tests
- **Auto Documentation**: OpenAPI/Swagger docs automatically generated

## Supported Models

### Text-to-Video (T2V)
- **Minimax T2V** (`/v1/t2v/minimax`)
- **Seedance V1 Lite** (`/v1/t2v/seedance-v1-lite`)

### Image-to-Video (I2V)
- **Kling 2.5** (`/v1/i2v/kling25`)
- **Minimax** (`/v1/i2v/minimax`)
- **Seedance** (`/v1/i2v/seedance`)
- **Veo3** (`/v1/i2v/veo3`)
- **Wan 2.5 Fast** (`/v1/i2v/wan25-fast`)

### Text-to-Image (T2I)
- **Nano Banana** (`/v1/t2i/nano-banana`)
- **Seedream 4** (`/v1/t2i/seedream4`)

### Job Management
- **Get Job Status** (`GET /v1/jobs/{job_set_id}`)
- **Refresh Job Status** (`POST /v1/jobs/{job_set_id}/refresh`)

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (optional)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/higgsfield-api.git
cd higgsfield-api
```

2. **Install dependencies**
```bash
pip install -e .

# For development
pip install -e ".[dev]"
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Run the service**
```bash
# Development
make run

# Or directly with uvicorn
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Docker Setup

### Development
```bash
# Start services
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Production
```bash
# Build production image
docker-compose --profile production build app-prod

# Start production services
docker-compose --profile production up -d app-prod
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

### Required Variables
```bash
# Higgsfield API Credentials
HF_API_KEY=c4a5848a-b2fb-4dd1-ad59-dcc1e2815833
HF_SECRET=8d43ce2938e1deb217d27358b48350d1e8937bd387996dc30571d747bffe13f4
```

### Optional Variables
```bash
# Retries
MAX_RETRIES=3
RETRY_BACKOFF_FACTOR=2.0

# Timeouts
REQUEST_TIMEOUT_CONNECT=10
REQUEST_TIMEOUT_READ=60

# Logging
LOG_LEVEL=INFO
LOG_JSON=false
```

## Usage Examples

### Text-to-Image (Nano Banana)

```bash
curl -X POST http://localhost:8000/v1/t2i/nano-banana \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "monkey sitting on a tree",
    "aspect_ratio": "4:3",
    "batch_size": 1
  }'
```

**Response:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_set_id": "hf-job-set-123",
  "status": "queued",
  "message": "T2I job submitted successfully"
}
```

### Image-to-Video (Kling 2.5)

```bash
curl -X POST http://localhost:8000/v1/i2v/kling25 \
  -H 'Content-Type: application/json' \
  -d '{
    "input_images": [
      {
        "type": "url",
        "image_url": "https://example.com/photo.jpg"
      }
    ],
    "prompt": "cinematic portrait with subtle camera motion",
    "aspect_ratio": "9:16",
    "motions": [
      {
        "id": "objects_around",
        "strength": 0.7
      }
    ]
  }'
```

### Text-to-Video (Minimax)

```bash
curl -X POST http://localhost:8000/v1/t2v/minimax \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "A cat playing piano in a jazz club",
    "aspect_ratio": "16:9"
  }'
```

### Get Job Status

```bash
curl -X GET http://localhost:8000/v1/jobs/hf-job-set-123
```

**Response:**
```json
{
  "id": "hf-job-set-123",
  "status": "completed",
  "jobs": [
    {
      "id": "job-1",
      "status": "completed",
      "progress": 100.0,
      "result": {
        "url": "https://cdn.higgsfield.ai/result.mp4"
      }
    }
  ]
}
```

## Development

### Run Tests

```bash
# All tests
make test

# Integration tests only
make test-integration

# With coverage
make test-cov
```

### Code Quality

```bash
# Format code
make fmt

# Lint
make lint

# Type check
make typecheck

# Run all checks
./scripts/run_tests.sh
```

### Project Structure

```
higgsfield-api/
├── app/
│   ├── core/              # Core modules (config, logging, errors)
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── errors.py
│   ├── schemas/           # Pydantic models
│   │   ├── common.py
│   │   ├── t2v.py
│   │   ├── i2v.py
│   │   ├── t2i.py
│   │   └── jobs.py
│   ├── clients/           # Higgsfield API clients
│   │   ├── higgsfield_base.py
│   │   ├── t2v_client.py
│   │   ├── i2v_client.py
│   │   ├── t2i_client.py
│   │   └── jobs_client.py
│   ├── services/          # Business logic
│   │   ├── t2v_service.py
│   │   ├── i2v_service.py
│   │   ├── t2i_service.py
│   │   └── jobs_service.py
│   ├── routers/           # FastAPI routers
│   │   ├── health.py
│   │   ├── t2v.py
│   │   ├── i2v.py
│   │   ├── t2i.py
│   │   └── jobs.py
│   ├── utils/             # Utilities
│   │   ├── retry.py
│   │   └── validators.py
│   └── main.py            # Application entry point
├── tests/
│   └── integration/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## API Documentation

When running in development mode, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

All errors return a consistent JSON format:

```json
{
  "error": {
    "message": "Error description",
    "code": "ErrorType",
    "details": {
      "field": "additional_info"
    }
  }
}
```

### Error Codes

- `422`: Validation error (invalid request data)
- `404`: Job not found
- `502`: Upstream API error
- `500`: Internal server error

## Logging

The service uses structured logging with the following fields:
- `timestamp`: ISO 8601 timestamp
- `level`: Log level (INFO, WARNING, ERROR)
- `logger`: Logger name
- `request_id`: Unique request identifier
- `duration_ms`: Request duration in milliseconds
- `method`: HTTP method
- `path`: Request path
- `status_code`: Response status code

### JSON Logging

Enable JSON logging for production:
```bash
LOG_JSON=true
```

## Deployment

### Docker Production Deployment

```bash
# Build production image
docker build --target production -t higgsfield-api:latest .

# Run container
docker run -d \
  --name higgsfield-api \
  -p 8000:8000 \
  --env-file .env \
  higgsfield-api:latest
```

### Environment Variables for Production

```bash
APP_ENV=production
APP_DEBUG=false
LOG_JSON=true
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com
```

### Health Checks

The `/health` endpoint can be used for health checks:
```bash
curl http://localhost:8000/health
```

Docker health check is configured automatically in the Dockerfile.

## Troubleshooting

### Common Issues

**Connection errors to Higgsfield API**
- Check `HF_API_KEY` and `HF_SECRET` are correct
- Verify network connectivity
- Check firewall rules

**Timeout errors**
- Increase `REQUEST_TIMEOUT_READ`
- Check Higgsfield API status
- Review retry settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run linters: `make lint && make typecheck`
6. Format code: `make fmt`
7. Submit a pull request

## License

MIT License

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Higgsfield AI](https://higgsfield.ai/)
