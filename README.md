# Higgsfield AI Chat

AI-powered chat interface for generating images and videos using Higgsfield's API.

## Quick Start

```bash
# 1. Setup environment
cp .env.example .env
# Add your HF_API_KEY, HF_SECRET, and GEMINI_API_KEY

# 2. Run with Docker
docker-compose up --build

# 3. Open frontend
python3 serve_frontend.py
# Visit http://localhost:8001
```

## Features

- **AI Chat Agent** - Natural conversation with Gemini 2.0
- **Image Generation** - Text-to-image with nano-banana
- **Video Generation** - Text-to-video with minimax
- **Image Animation** - Image-to-video with kling25
- **Real-time Status** - Auto-polling for job completion

## API Endpoints

- `POST /v1/chat` - Chat with AI agent
- `GET /v1/jobs/{job_id}` - Check job status
- `GET /health` - Health check

## Tech Stack

- **Backend**: FastAPI + LangGraph + Gemini
- **Frontend**: Vanilla HTML/JS
- **API**: Higgsfield Platform

## Development

```bash
# Run locally
python -m venv venv
source venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```
