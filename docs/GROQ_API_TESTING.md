# Groq API Testing Guide

## Quick Test Script

We've created a test script for you. Just run:

```bash
./test_groq_api.sh
```

This will automatically load your API key from `.env` and test the connection.

---

## Manual cURL Commands

### 1. Basic Test (Simple Chat Completion)

```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY_HERE" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {
        "role": "user",
        "content": "Hello! Can you confirm the API is working?"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### 2. Test with System Prompt (Interview Agent Style)

```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY_HERE" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {
        "role": "system",
        "content": "You are a Senior Technical Recruiter analyzing job descriptions."
      },
      {
        "role": "user",
        "content": "Analyze this job requirement: 5+ years Python experience, Django, PostgreSQL"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### 3. List Available Models

```bash
curl -X GET "https://api.groq.com/openai/v1/models" \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY_HERE" \
  -H "Content-Type: application/json"
```

### 4. Test with Environment Variable

If you have your API key in `.env`, you can use:

```bash
# Load environment variables
source .env

# Make the API call
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -d "{
    \"model\": \"$GROQ_MODEL_NAME\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"Test message\"
      }
    ],
    \"temperature\": 0.7
  }"
```

### 5. Pretty Print with jq

For better formatted output, pipe to `jq`:

```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY_HERE" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }' | jq '.'
```

---

## Available Models on Groq

You can use these models by changing the `GROQ_MODEL_NAME` in your `.env`:

- **llama-3.3-70b-versatile** (default, recommended)
- **llama-3.1-70b-versatile**
- **llama-3.1-8b-instant**
- **mixtral-8x7b-32768**
- **gemma-7b-it**
- **gemma2-9b-it**

---

## Expected Response Format

A successful response looks like:

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "llama-3.3-70b-versatile",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! The API is working correctly!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 10,
    "total_tokens": 25
  }
}
```

---

## Common Error Responses

### Invalid API Key

```json
{
  "error": {
    "message": "Invalid API Key",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

**Solution:** Check your API key in `.env` file

### Rate Limit Exceeded

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error"
  }
}
```

**Solution:** Wait a moment and try again, or upgrade your Groq plan

### Invalid Model

```json
{
  "error": {
    "message": "Model not found",
    "type": "invalid_request_error"
  }
}
```

**Solution:** Check the model name matches one of the available models

---

## Testing Your Python Integration

After confirming the API works with curl, test your Python integration:

```bash
# Simple Python test
python -c "from src.config import get_llm; llm = get_llm(); print(llm.invoke('Hello!').content)"
```

Or run the full example:

```bash
python -m src.main example
```

---

## Monitoring API Usage

You can monitor your API usage at:

- **Groq Console:** https://console.groq.com/

This shows:

- Request count
- Token usage
- Rate limits
- Billing information

---

## Tips for Testing

1. **Start Simple:** Use the basic test first to confirm connectivity
2. **Check Logs:** Look for helpful error messages in the response
3. **Verify Environment:** Make sure `.env` is loaded correctly
4. **Test Incrementally:** Test curl → Python → Full application
5. **Monitor Tokens:** Keep an eye on token usage for cost management

---

## Quick Troubleshooting

| Issue                   | Solution                                 |
| ----------------------- | ---------------------------------------- |
| "command not found: jq" | Install jq: `brew install jq` (macOS)    |
| "Invalid API Key"       | Check `.env` file has correct key        |
| "Connection refused"    | Check internet connection                |
| "Rate limit exceeded"   | Wait 60 seconds and retry                |
| No response             | Add `-v` flag to curl for verbose output |

---

## Next Steps

Once the API test succeeds:

1. ✅ Update your `.env` with the working API key
2. ✅ Run `./setup_groq.sh` to install dependencies
3. ✅ Test Python integration: `python -m src.main example`
4. ✅ Start the server: `./start_server.sh`
5. ✅ Access the API at http://localhost:8000/docs
