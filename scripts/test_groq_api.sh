#!/bin/bash

# Test Groq API Connection
# This script tests if your Groq API key is working correctly

echo "🧪 Testing Groq API Connection"
echo "================================"
echo ""

# Load API key from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ Error: .env file not found"
    exit 1
fi

# Check if API key is set
if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_groq_api_key_here" ]; then
    echo "❌ Error: GROQ_API_KEY not configured"
    echo "Please update your .env file with your Groq API key"
    exit 1
fi

echo "🔑 API Key found: ${GROQ_API_KEY:0:20}..."
echo "🤖 Model: ${GROQ_MODEL_NAME:-llama-3.3-70b-versatile}"
echo ""
echo "📡 Sending test request to Groq API..."
echo ""

# Test API call
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -d "{
    \"model\": \"${GROQ_MODEL_NAME:-llama-3.3-70b-versatile}\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a helpful assistant.\"
      },
      {
        \"role\": \"user\",
        \"content\": \"Say 'Hello! Groq API is working correctly!' in a friendly way.\"
      }
    ],
    \"temperature\": 0.7,
    \"max_tokens\": 100
  }" | jq '.'

echo ""
echo ""
echo "✅ If you see a response above, your Groq API is working!"
echo "❌ If you see an error, check your API key and try again."
