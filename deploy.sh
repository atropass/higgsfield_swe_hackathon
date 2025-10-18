set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE} Deploying Higgsfield AI Chat to Cloud Run${NC}"

if [ -z "$HF_API_KEY" ] || [ -z "$HF_SECRET" ] || [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: Required environment variables not set"
    echo "Please set: HF_API_KEY, HF_SECRET, GEMINI_API_KEY"
    echo ""
    echo "Example:"
    echo "export HF_API_KEY=your-key"
    echo "export HF_SECRET=your-secret"
    echo "export GEMINI_API_KEY=your-gemini-key"
    exit 1
fi

PROJECT_ID=$(gcloud config get-value project)
echo -e "${GREEN} Project: ${PROJECT_ID}${NC}"

REGION=${REGION:-us-central1}
echo -e "${GREEN} Region: ${REGION}${NC}"

SERVICE_NAME="higgsfield-ai-chat"

echo -e "${BLUE} Building and deploying...${NC}"

gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars="HF_API_KEY=${HF_API_KEY},HF_SECRET=${HF_SECRET},GEMINI_API_KEY=${GEMINI_API_KEY},APP_ENV=production,APP_DEBUG=true,LOG_JSON=true" \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --port 8000

SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format='value(status.url)')

echo ""
echo -e "${GREEN} Deployment successful!${NC}"
echo ""
echo -e "${BLUE} Service URL:${NC} ${SERVICE_URL}"
echo -e "${BLUE} API Docs:${NC} ${SERVICE_URL}/docs"
echo -e "${BLUE} Health:${NC} ${SERVICE_URL}/health"
echo ""
echo -e "${GREEN} Your Higgsfield AI Chat is live!${NC}"

