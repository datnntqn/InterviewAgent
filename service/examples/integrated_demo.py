"""
Demo: CrewAI + LangGraph Integration
Workflow kết hợp: Tạo câu hỏi với CrewAI, phỏng vấn với LangGraph
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

# Sample data
JOB_DESCRIPTION = """
Senior Python Developer

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Django or Flask
- Experience with PostgreSQL and Redis
- Familiarity with Docker and Kubernetes
- Understanding of RESTful API design
"""

USER_CV = """
John Doe - Software Engineer

Experience:
- 6 years of Python development
- Proficient in Django and Flask
- Worked with PostgreSQL, MySQL
- Experience with Docker
- Built multiple RESTful APIs
"""

def print_separator():
    print("\n" + "="*80 + "\n")

def combined_workflow_demo():
    """Demo using combined endpoint (recommended)"""
    print("🚀 DEMO: Combined CrewAI + LangGraph Workflow")
    print_separator()
    
    # Step 1: Call combined endpoint
    print("📞 Calling /api/prepare-and-start...")
    print("   This will:")
    print("   1. Generate questions with CrewAI")
    print("   2. Start LangGraph interactive session")
    print("   (This may take 30-60 seconds...)")
    print_separator()
    
    response = requests.post(
        f"{API_BASE}/api/prepare-and-start",
        json={
            "job_description": JOB_DESCRIPTION,
            "user_cv": USER_CV,
            "company_name": "TechCorp",
            "company_website": "https://techcorp.com",
            "tone": "friendly",
            "level": "senior",
            "interview_type": "mixed"
        },
        timeout=300
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    
    # Display results
    print("✅ Setup Complete!")
    print_separator()
    
    print("📊 CrewAI Analysis:")
    crewai_result = data["crewai_result"]["result"]
    
    if "interview_strategy" in crewai_result:
        strategy = crewai_result["interview_strategy"]
        print(f"   Roadmap Items: {len(strategy.get('preparation_roadmap', []))}")
        print(f"   Key Points: {len(strategy.get('key_talking_points', []))}")
    
    print(f"\n💬 LangGraph Session:")
    print(f"   Thread ID: {data['thread_id']}")
    print(f"   Total Questions: {data['total_questions']}")
    
    print_separator()
    print(f"❓ Question 1/{data['total_questions']}:")
    print(f"   {data['first_question']}")
    print_separator()
    
    # Interactive Q&A
    thread_id = data["thread_id"]
    question_num = 1
    
    while True:
        answer = input("💬 Your answer (or 'quit' to exit): ")
        
        if answer.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Exiting interview...")
            break
        
        # Submit answer
        print("\n⏳ Evaluating your answer...")
        response = requests.post(
            f"{API_BASE}/api/interview/chat/{thread_id}",
            json={"answer": answer}
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            break
        
        result = response.json()
        
        # Show feedback
        print_separator()
        print("📈 Evaluation:")
        print(f"   Score: {result['feedback']['score']}/10")
        print(f"   Feedback: {result['feedback']['feedback']}")
        
        if result['feedback'].get('strengths'):
            print(f"   ✅ Strengths: {', '.join(result['feedback']['strengths'])}")
        
        if result['feedback'].get('improvements'):
            print(f"   ⚠️  Improvements: {', '.join(result['feedback']['improvements'])}")
        
        print_separator()
        
        if result['interview_complete']:
            print("✅ Interview Complete!")
            break
        
        # Next question
        question_num += 1
        print(f"❓ Question {result['progress']['current']}/{result['progress']['total']}:")
        print(f"   {result['next_question']}")
        print_separator()
    
    # Get summary
    print("\n📊 Fetching final summary...")
    summary = requests.get(f"{API_BASE}/api/interview/summary/{thread_id}").json()
    
    print_separator()
    print("🎯 FINAL INTERVIEW SUMMARY")
    print_separator()
    print(f"Overall Score: {summary['overall_score']}/10")
    print(f"Total Questions: {summary['total_questions']}")
    
    print("\n📊 Performance Breakdown:")
    breakdown = summary['performance_breakdown']
    print(f"   Technical Average: {breakdown['technical_avg']}/10")
    print(f"   Behavioral Average: {breakdown['behavioral_avg']}/10")
    
    print("\n✅ Strengths:")
    for strength in summary['strengths']:
        print(f"   • {strength}")
    
    print("\n⚠️  Areas for Improvement:")
    for area in summary['areas_for_improvement']:
        print(f"   • {area}")
    
    print("\n💡 Recommendations:")
    for rec in summary['recommendations']:
        print(f"   • {rec}")
    
    print_separator()

def two_step_workflow_demo():
    """Demo using separate endpoints"""
    print("🚀 DEMO: Two-Step Workflow (CrewAI → LangGraph)")
    print_separator()
    
    # Step 1: CrewAI
    print("📞 Step 1: Calling CrewAI /api/prepare...")
    response = requests.post(
        f"{API_BASE}/api/prepare",
        json={
            "job_description": JOB_DESCRIPTION,
            "user_cv": USER_CV,
            "company_name": "TechCorp",
            "company_website": "https://techcorp.com",
            "tone": "friendly",
            "level": "senior",
            "interview_type": "mixed"
        },
        timeout=300
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return
    
    crewai_result = response.json()
    print("✅ CrewAI questions generated!")
    
    # Step 2: LangGraph
    print("\n📞 Step 2: Starting LangGraph session...")
    response = requests.post(
        f"{API_BASE}/api/interview/start",
        json={
            "crewai_result": crewai_result.get("result", {}),
            "job_description": JOB_DESCRIPTION,
            "user_cv": USER_CV,
            "company_name": "TechCorp",
            "tone": "friendly",
            "level": "senior"
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return
    
    session_data = response.json()
    print("✅ LangGraph session started!")
    print(f"   Thread ID: {session_data['thread_id']}")
    print(f"   First Question: {session_data['first_question']}")
    
    print_separator()
    print("✅ Two-step workflow complete!")
    print("   You can now use /api/interview/chat/{thread_id} to continue")

def main():
    print("\n" + "="*80)
    print("   CrewAI + LangGraph Integration Demo")
    print("="*80 + "\n")
    
    print("Choose demo mode:")
    print("1. Combined Workflow (Recommended) - One API call")
    print("2. Two-Step Workflow - Separate CrewAI and LangGraph calls")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        combined_workflow_demo()
    elif choice == "2":
        two_step_workflow_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interview interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
