#!/usr/bin/env python3
"""
Quick test to verify Google Gemini integration works.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

print("🧪 Testing Google Gemini Integration\n")
print("=" * 60)

# Test 1: Config loading
print("\n1️⃣  Testing configuration...")
try:
    from src.config import Settings, get_llm
    settings = Settings()
    
    print(f"   ✅ Google API Key: {settings.google_api_key[:20]}..." if settings.google_api_key else "   ❌ No Google API Key")
    print(f"   ✅ Model: {settings.groq_model_name}")
    
    # Test LLM initialization
    llm_string = get_llm(temperature=0.7)
    print(f"   ✅ LLM String: {llm_string}")
    
    if "gemini" in llm_string:
        print("   ✅ Using Google Gemini provider")
    else:
        print("   ⚠️  Not using Gemini - check GROQ_MODEL_NAME")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Agent creation
print("\n2️⃣  Testing agent creation...")
try:
    from src.agents import InterviewAgents
    
    agents = InterviewAgents(tone="friendly", level="mid")
    jd_analyst = agents.jd_analyst()
    
    print(f"   ✅ Agent created: {jd_analyst.role}")
    print(f"   ✅ Agent LLM: {jd_analyst.llm}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Simple API call (optional - requires actual API call)
print("\n3️⃣  Testing simple LLM call...")
try:
    # This will make a real API call
    print("   ⏳ Making test API call to Gemini...")
    
    from crewai import Agent, Task, Crew
    
    test_agent = Agent(
        role="Test Agent",
        goal="Say hello",
        backstory="You are a test agent",
        llm=llm_string,
        verbose=False
    )
    
    test_task = Task(
        description="Say 'Hello from Gemini!' in exactly 5 words or less.",
        expected_output="A short greeting",
        agent=test_agent
    )
    
    crew = Crew(
        agents=[test_agent],
        tasks=[test_task],
        verbose=False
    )
    
    result = crew.kickoff()
    print(f"   ✅ Gemini response: {str(result)[:100]}")
    print("   ✅ API call successful!")
    
except Exception as e:
    error_str = str(e)
    if "rate_limit" in error_str.lower():
        print(f"   ❌ Rate limit error (shouldn't happen with Gemini!): {e}")
    elif "api_key" in error_str.lower() or "authentication" in error_str.lower():
        print(f"   ❌ API key error: {e}")
        print("   💡 Check your GOOGLE_API_KEY in .env")
    else:
        print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! Google Gemini is working correctly.")
print("\n💡 Next steps:")
print("   1. Test full workflow in Streamlit UI")
print("   2. Submit an interview preparation request")
print("   3. Verify no 429 rate limit errors")
print("   4. Check response quality")
print()
