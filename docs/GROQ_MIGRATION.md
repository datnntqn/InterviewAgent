# Groq Cloud API Migration Guide

## Overview

This document summarizes the migration from **Local Ollama (Llama 3)** to **Groq Cloud API** for LLM inference.

## ✅ Completed Changes

### 1. Dependencies Updated

**File:** `requirements.txt`

- ✅ Added `langchain-groq>=0.1.0`
- ✅ Kept `langchain-community>=0.1.0` for compatibility

### 2. Environment Configuration

**File:** `.env.example`

- ✅ Removed Ollama-specific variables (`OLLAMA_BASE_URL`, `OLLAMA_HOST`, `LLM_MODEL`)
- ✅ Added Groq configuration:
  ```env
  GROQ_API_KEY=your_groq_api_key_here
  GROQ_MODEL_NAME=llama-3.3-70b-versatile
  ```

### 3. Centralized LLM Configuration

**File:** `src/config.py`

- ✅ Replaced `Settings` class to use Groq configuration
- ✅ Created `get_llm()` factory function that:
  - Loads `GROQ_API_KEY` and `GROQ_MODEL_NAME` from environment
  - Initializes `ChatGroq` with `temperature=0.7`
  - Validates API key and provides helpful error messages
  - Uses `llama-3.3-70b-versatile` as default model

### 4. Agents Refactored

**File:** `src/agents/agents.py`

- ✅ Removed `ChatOllama` imports and Ollama-specific code
- ✅ Imported `get_llm` from `src/config.py`
- ✅ Updated `InterviewAgents.__init__()` to use `self.llm = get_llm(temperature=0.7)`
- ✅ All agents (`jd_analyst`, `corporate_researcher`, `lead_interviewer`) now use Groq

### 5. Main Entry Point Updated

**File:** `src/main.py`

- ✅ Updated logging to show Groq configuration instead of Ollama
- ✅ Logs now display: `Groq Model: llama-3.3-70b-versatile` and `Using Groq Cloud API for LLM inference`

### 6. Crew Configuration Updated

**File:** `src/crews/interview_crew.py`

- ✅ Removed Ollama-specific embedder configuration
- ✅ Crew now uses default embeddings (can be configured separately if needed)

### 7. Docker Cleanup

**File:** `docker-compose.yml`

- ✅ Removed the entire `ollama` service (saves significant resources)
- ✅ Removed `ollama_data` volume
- ✅ Removed `depends_on` condition for Ollama
- ✅ Updated `app` service to use Groq environment variables
- ✅ Added `env_file: .env` to load environment variables

## 📋 Manual Steps Required

### Step 1: Get Your Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in to your Groq account
3. Create a new API key
4. Copy the API key (you won't be able to see it again!)

### Step 2: Update Your .env File

Create or update your `.env` file in the project root:

```bash
# Copy from example
cp .env.example .env

# Edit the .env file and add your actual API key
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

⚠️ **IMPORTANT:** Never commit your `.env` file with the actual API key to version control!

### Step 3: Install Updated Dependencies

```bash
# If using virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install new dependencies
pip install -r requirements.txt
```

### Step 4: Clean Up Docker (Optional)

If you were using Docker with Ollama, you can clean up old resources:

```bash
# Stop and remove containers
docker-compose down

# Remove Ollama volume (if it exists)
docker volume rm interview-agent_ollama_data

# Rebuild with new configuration
docker-compose build
docker-compose up
```

### Step 5: Test the Migration

Run a test to ensure everything works:

```bash
# Test with example data
python -m src.main example

# Or run in interactive mode
python -m src.main interactive
```

## 🎯 Benefits of This Migration

1. **Performance**: Groq Cloud API is significantly faster than local Ollama
2. **Resource Efficiency**: No need to run heavy local LLM models
3. **Scalability**: Cloud-based inference scales automatically
4. **Model Access**: Easy access to latest Llama 3.3 70B model
5. **Simplified Deployment**: No Docker GPU configuration needed

## 🔧 Configuration Options

### Available Groq Models

You can change the model by updating `GROQ_MODEL_NAME` in your `.env` file:

- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

### Temperature Setting

The default temperature is `0.7` (balanced creativity/consistency). To change it, modify `src/config.py`:

```python
def get_llm(temperature: float = 0.7) -> ChatGroq:
    # Change the default value here
```

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY is not set"

- Make sure you've created a `.env` file in the project root
- Verify the API key is set correctly in `.env`
- Don't use the placeholder value `your_groq_api_key_here`

### Error: "Invalid API key"

- Check that you copied the API key correctly from Groq console
- Ensure there are no extra spaces or quotes around the key
- Verify your Groq account is active

### Error: "Rate limit exceeded"

- Groq has rate limits on free tier
- Consider upgrading your Groq plan or implementing retry logic
- Add delays between requests if processing multiple interviews

## 📚 Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [LangChain Groq Integration](https://python.langchain.com/docs/integrations/chat/groq)
- [CrewAI Documentation](https://docs.crewai.com/)

## 🔄 Rollback Instructions

If you need to rollback to Ollama for any reason:

1. Restore the original files from git:

   ```bash
   git checkout HEAD -- requirements.txt .env.example src/config.py src/agents/agents.py src/main.py src/crews/interview_crew.py docker-compose.yml
   ```

2. Reinstall dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama service:
   ```bash
   docker-compose up -d ollama
   ```

---

**Migration completed on:** 2026-01-13  
**Migrated by:** Senior Python Backend Engineer  
**Status:** ✅ Ready for Testing
