"""
Example usage of the LangGraph Interactive Interview System

This script demonstrates how to use the new interactive interview endpoints.
"""

import requests
import json
import time

# Configuration
API_BASE = "http://localhost:8000/api/interview"

# Sample data
JOB_DESCRIPTION = """
Senior Python Developer

We are looking for an experienced Python developer to join our team.

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Django or Flask
- Experience with PostgreSQL and Redis
- Familiarity with Docker and Kubernetes
- Understanding of RESTful API design
- Experience with CI/CD pipelines

Nice to have:
- Experience with React or Vue.js
- Knowledge of AWS or GCP
- Contributions to open-source projects
"""

USER_CV = """
John Doe - Software Engineer

Experience:
- 6 years of Python development
- Proficient in Django and Flask
- Worked with PostgreSQL, MySQL, and MongoDB
- Experience with Docker
- Built multiple RESTful APIs
- Some experience with React

Skills:
Python, Django, Flask, PostgreSQL, Docker, Git, REST APIs, React

Projects:
- E-commerce platform using Django
- Microservices architecture with Flask
- Database optimization for high-traffic applications
"""

# Sample answers for automated testing
SAMPLE_ANSWERS = [
    "I have 6 years of Python experience, primarily using Django for building web applications. I've worked on e-commerce platforms and microservices architectures.",
    "I follow RESTful principles: using proper HTTP methods, stateless design, resource-based URLs, and JSON for data exchange. I also implement versioning and proper error handling.",
    "I faced a situation where our API was slow. I profiled the code, identified N+1 queries, implemented select_related and prefetch_related, and added Redis caching. Response time improved by 70%.",
    "I use Docker for containerization and have experience with Kubernetes for orchestration. I've set up CI/CD pipelines using GitLab CI and deployed to AWS ECS.",
    "I had a disagreement with a teammate about architecture. I scheduled a meeting, presented data supporting my approach, listened to their concerns, and we found a hybrid solution that addressed both viewpoints.",
    "I'm excited about TechCorp's focus on innovation and the opportunity to work on scalable systems. I admire your open-source contributions and would love to be part of that culture.",
]


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*80 + "\n")


def start_interview():
    """Start a new interview session"""
    print("🚀 Starting new interview session...")
    
    response = requests.post(
        f"{API_BASE}/start",
        json={
            "job_description": JOB_DESCRIPTION,
            "user_cv": USER_CV,
            "company_name": "TechCorp",
            "company_website": "https://techcorp.com",
            "tone": "friendly",
            "level": "senior"
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    
    print(f"✅ Session started!")
    print(f"📋 Thread ID: {data['thread_id']}")
    print(f"📊 Total Questions: {data['total_questions']}")
    print_separator()
    print(f"❓ Question 1/{data['total_questions']}:")
    print(f"   {data['first_question']}")
    print_separator()
    
    return data


def submit_answer(thread_id, answer, question_num):
    """Submit an answer to the current question"""
    print(f"💬 Submitting answer to question {question_num}...")
    print(f"   Answer: {answer[:100]}...")
    
    response = requests.post(
        f"{API_BASE}/chat/{thread_id}",
        json={"answer": answer}
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    
    print_separator()
    print("📈 Evaluation:")
    print(f"   Score: {data['feedback']['score']}/10")
    print(f"   Feedback: {data['feedback']['feedback']}")
    
    if data['feedback'].get('strengths'):
        print(f"   ✅ Strengths: {', '.join(data['feedback']['strengths'])}")
    
    if data['feedback'].get('improvements'):
        print(f"   ⚠️  Improvements: {', '.join(data['feedback']['improvements'])}")
    
    print_separator()
    
    if not data['interview_complete']:
        print(f"❓ Question {data['progress']['current']}/{data['progress']['total']}:")
        print(f"   {data['next_question']}")
        print_separator()
    else:
        print("✅ Interview Complete!")
        print_separator()
    
    return data


def get_summary(thread_id):
    """Get the final interview summary"""
    print("📊 Fetching final summary...")
    
    response = requests.get(f"{API_BASE}/summary/{thread_id}")
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    
    print_separator()
    print("🎯 FINAL INTERVIEW SUMMARY")
    print_separator()
    print(f"Overall Score: {data['overall_score']}/10")
    print(f"Total Questions: {data['total_questions']}")
    
    print("\n📊 Performance Breakdown:")
    breakdown = data['performance_breakdown']
    print(f"   Technical Average: {breakdown['technical_avg']}/10")
    print(f"   Behavioral Average: {breakdown['behavioral_avg']}/10")
    
    print("\n✅ Strengths:")
    for strength in data['strengths']:
        print(f"   • {strength}")
    
    print("\n⚠️  Areas for Improvement:")
    for area in data['areas_for_improvement']:
        print(f"   • {area}")
    
    print("\n💡 Recommendations:")
    for rec in data['recommendations']:
        print(f"   • {rec}")
    
    print_separator()
    
    return data


def run_automated_interview():
    """Run a complete automated interview using sample answers"""
    print("🤖 Running Automated Interview Demo")
    print_separator()
    
    # Start interview
    session = start_interview()
    if not session:
        return
    
    thread_id = session['thread_id']
    total_questions = session['total_questions']
    
    # Answer each question
    for i, answer in enumerate(SAMPLE_ANSWERS[:total_questions], start=1):
        time.sleep(1)  # Brief pause between questions
        
        result = submit_answer(thread_id, answer, i)
        if not result:
            break
        
        if result['interview_complete']:
            break
    
    # Get final summary
    time.sleep(1)
    get_summary(thread_id)


def run_interactive_interview():
    """Run an interactive interview where user types answers"""
    print("👤 Running Interactive Interview")
    print_separator()
    
    # Start interview
    session = start_interview()
    if not session:
        return
    
    thread_id = session['thread_id']
    question_num = 1
    
    # Answer each question
    while True:
        answer = input("\n💬 Your answer: ")
        
        if answer.lower() in ['quit', 'exit', 'q']:
            print("👋 Exiting interview...")
            break
        
        result = submit_answer(thread_id, answer, question_num)
        if not result:
            break
        
        question_num += 1
        
        if result['interview_complete']:
            break
    
    # Get final summary
    time.sleep(1)
    get_summary(thread_id)


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("   AI Mock Interview Agent - LangGraph Interactive Demo")
    print("="*80 + "\n")
    
    print("Choose mode:")
    print("1. Automated Demo (uses sample answers)")
    print("2. Interactive Mode (you type answers)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_automated_interview()
    elif choice == "2":
        run_interactive_interview()
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
