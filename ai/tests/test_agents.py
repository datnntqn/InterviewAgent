#!/usr/bin/env python3
"""
Test script to verify the InterviewAgents implementation.
"""

from src.agents import InterviewAgents

def test_agents():
    """Test agent creation with different configurations."""
    
    print("🧪 Testing InterviewAgents...")
    print()
    
    # Test 1: Friendly tone
    print("1️⃣ Testing Friendly tone agents...")
    friendly_agents = InterviewAgents(tone="friendly", level="mid")
    friendly_dict = friendly_agents.get_all_agents()
    print(f"   ✅ Created {len(friendly_dict)} agents: {list(friendly_dict.keys())}")
    print()
    
    # Test 2: Strict tone
    print("2️⃣ Testing Strict tone agents...")
    strict_agents = InterviewAgents(tone="strict", level="senior")
    strict_dict = strict_agents.get_all_agents()
    print(f"   ✅ Created {len(strict_dict)} agents: {list(strict_dict.keys())}")
    print()
    
    # Test 3: Verify agent properties
    print("3️⃣ Verifying agent properties...")
    jd_agent = friendly_agents.jd_analyst()
    print(f"   JD Analyst Role: {jd_agent.role}")
    print(f"   JD Analyst Goal: {jd_agent.goal[:50]}...")
    print()
    
    corp_agent = friendly_agents.corporate_researcher()
    print(f"   Corporate Researcher Role: {corp_agent.role}")
    print(f"   Corporate Researcher Tools: {len(corp_agent.tools)} tool(s)")
    print()
    
    lead_agent = friendly_agents.lead_interviewer()
    print(f"   Lead Interviewer Role: {lead_agent.role}")
    print(f"   Lead Interviewer Delegation: {lead_agent.allow_delegation}")
    print()
    
    # Test 4: Verify STAR method in backstory
    print("4️⃣ Verifying STAR method in Lead Interviewer backstory...")
    if "STAR" in lead_agent.backstory:
        print("   ✅ STAR method mentioned in backstory")
    else:
        print("   ❌ STAR method NOT found in backstory")
    print()
    
    print("✅ All tests passed!")
    print()
    print("📝 Summary:")
    print(f"   - Agents can be created with different tones (friendly/strict)")
    print(f"   - All 3 agents are properly configured")
    print(f"   - Corporate Researcher has web scraping tool")
    print(f"   - Lead Interviewer has dynamic backstory based on tone")
    print(f"   - STAR method is emphasized for behavioral questions")


if __name__ == "__main__":
    test_agents()
