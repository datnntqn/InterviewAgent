#!/usr/bin/env python3
"""
Quick test script to verify the complete CrewAI implementation.
"""

import sys
sys.path.insert(0, '.')

from src.agents import InterviewAgents
from src.tasks import InterviewTasks
from src.crews import InterviewPreparationCrew

def test_components():
    """Test individual components."""
    print("🧪 Testing CrewAI Components...\n")
    
    # Test 1: Agents
    print("1️⃣ Testing Agents...")
    try:
        agents_factory = InterviewAgents(tone="friendly", level="mid")
        agents = agents_factory.get_all_agents()
        print(f"   ✅ Created {len(agents)} agents: {list(agents.keys())}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 2: Tasks
    print("2️⃣ Testing Tasks...")
    try:
        tasks_factory = InterviewTasks()
        print("   ✅ Tasks factory initialized\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 3: Crew
    print("3️⃣ Testing Crew...")
    try:
        crew = InterviewPreparationCrew(tone="friendly", level="mid", verbose=False)
        print("   ✅ Crew initialized\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    print("✅ All component tests passed!\n")
    return True


def main():
    """Run tests."""
    print("\n" + "="*60)
    print("🎯 AI Mock Interview Agent - Component Tests")
    print("="*60 + "\n")
    
    success = test_components()
    
    if success:
        print("="*60)
        print("✅ System Ready!")
        print("="*60)
        print("\n📝 Next steps:")
        print("  1. Ensure Ollama is running: docker-compose up ollama -d")
        print("  2. Run example: python -m src.main example")
        print("  3. Run interactive: python -m src.main interactive")
        print("\n" + "="*60 + "\n")
    else:
        print("="*60)
        print("❌ Tests Failed")
        print("="*60)
        print("\nPlease check the errors above and fix them.\n")


if __name__ == "__main__":
    main()
