set -e

echo "Starting Higgsfield API in development mode..."

if [ -f .env ]; then
    echo "Loading .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "Starting uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

