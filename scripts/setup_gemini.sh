#!/bin/bash
# Interactive setup script for Google Gemini API
# This script helps you quickly switch from Groq to Gemini

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 Google Gemini Setup - AI Mock Interview Agent       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please create .env from .env.example first"
    exit 1
fi

echo "📋 Why Google Gemini?"
echo "   • TPM Limit: 250,000 (vs Groq's 20,000)"
echo "   • No rate limit errors"
echo "   • Faster responses"
echo "   • 100% FREE"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Get your FREE Google API Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Open: https://aistudio.google.com/apikey"
echo "2. Login with your Google account"
echo "3. Click 'Create API Key'"
echo "4. Copy the key (starts with AIza...)"
echo ""

read -p "Press Enter when you have your API key ready..."
echo ""

# Prompt for API key
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Enter your API Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Paste your Google API key here: " GOOGLE_KEY

if [ -z "$GOOGLE_KEY" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Validate key format
if [[ ! $GOOGLE_KEY =~ ^AIza ]]; then
    echo "⚠️  Warning: Key doesn't start with 'AIza'. Are you sure it's correct?"
    read -p "Continue anyway? (y/n): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo "Exiting."
        exit 1
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Updating Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Backup current .env
BACKUP_FILE=".env.backup.$(date +%Y%m%d_%H%M%S)"
cp .env "$BACKUP_FILE"
echo "✅ Backed up .env to: $BACKUP_FILE"

# Add or update Google API key
if grep -q "^GOOGLE_API_KEY=" .env; then
    # Update existing
    sed -i '' "s|^GOOGLE_API_KEY=.*|GOOGLE_API_KEY=$GOOGLE_KEY|" .env
    echo "✅ Updated existing GOOGLE_API_KEY"
else
    # Add new
    echo "" >> .env
    echo "# Google Gemini API (250k TPM - Best free option!)" >> .env
    echo "GOOGLE_API_KEY=$GOOGLE_KEY" >> .env
    echo "✅ Added GOOGLE_API_KEY to .env"
fi

# Update model name to use Gemini
if grep -q "^GROQ_MODEL_NAME=" .env; then
    sed -i '' "s|^GROQ_MODEL_NAME=.*|GROQ_MODEL_NAME=gemini-1.5-flash|" .env
    echo "✅ Updated GROQ_MODEL_NAME to gemini-1.5-flash"
else
    echo "GROQ_MODEL_NAME=gemini-1.5-flash" >> .env
    echo "✅ Added GROQ_MODEL_NAME=gemini-1.5-flash"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Show current config
echo "📋 Current Configuration:"
echo ""
grep "^GROQ_MODEL_NAME=" .env
grep "^GOOGLE_API_KEY=" .env | sed "s/\(GOOGLE_API_KEY=AIza[a-zA-Z0-9]\{10\}\).*/\1.../"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Restart Backend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Restart backend now? (y/n): " restart
if [[ $restart =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Restarting backend..."
    
    # Kill existing backend
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
    
    # Start backend
    echo "🚀 Starting backend with Gemini..."
    nohup python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    
    sleep 3
    
    # Check if backend is running
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend started successfully!"
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║                    🎉 Setup Complete!                     ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        echo "✨ You're now using Google Gemini with 250k TPM!"
        echo ""
        echo "📊 Benefits:"
        echo "   • No more rate limit errors (429)"
        echo "   • Faster response times"
        echo "   • Can handle multiple requests"
        echo ""
        echo "🧪 Test it now:"
        echo "   • Open Streamlit UI"
        echo "   • Submit an interview preparation request"
        echo "   • Watch it complete without errors!"
        echo ""
        echo "📝 Logs: tail -f backend.log"
        echo ""
    else
        echo "⚠️  Backend may not have started correctly"
        echo "   Check logs: tail -f backend.log"
    fi
else
    echo ""
    echo "⚠️  Remember to restart backend manually:"
    echo "   ./scripts/restart-be.sh"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Rollback Instructions:"
echo "   If you want to switch back to Groq:"
echo "   1. Restore backup: cp $BACKUP_FILE .env"
echo "   2. Restart backend: ./scripts/restart-be.sh"
echo ""
