"""
LLM Prompts for LangGraph Interview Nodes

This module contains all prompts used by the interview graph nodes.
"""

GENERATE_QUESTIONS_PROMPT = """You are an expert technical interviewer preparing questions for a candidate.

**Job Description:**
{job_description}

**Candidate's CV:**
{user_cv}

**Company:** {company_name}
**Interview Tone:** {tone}
**Experience Level:** {level}

**Task:** Generate 6-8 interview questions that:
1. Mix technical (60%) and behavioral (40%) questions
2. Are tailored to the candidate's background and the job requirements
3. Progress from easier to harder
4. For behavioral questions, can be evaluated using the STAR method

**Output Format (JSON):**
```json
{{
  "questions": [
    {{
      "question": "The question text",
      "type": "technical" or "behavioral",
      "expected_points": ["point1", "point2", "point3"],
      "difficulty": "easy" or "medium" or "hard"
    }}
  ]
}}
```

Generate questions that will help assess if this candidate is a good fit for the role."""

EVALUATE_TECHNICAL_ANSWER_PROMPT = """You are evaluating a candidate's answer to a technical interview question.

**Question:** {question}

**Expected Key Points:**
{expected_points}

**Candidate's Answer:**
{user_answer}

**Evaluation Criteria:**
- Technical accuracy (40%)
- Depth of understanding (30%)
- Communication clarity (20%)
- Practical examples (10%)

**Provide:**
1. Score (0-10)
2. Strengths in the answer
3. Areas for improvement
4. Constructive feedback

**Output Format (JSON):**
```json
{{
  "score": 8.5,
  "strengths": ["point1", "point2"],
  "improvements": ["area1", "area2"],
  "feedback": "Detailed constructive feedback..."
}}
```"""

EVALUATE_BEHAVIORAL_ANSWER_PROMPT = """You are evaluating a candidate's answer to a behavioral interview question using the STAR method.

**Question:** {question}

**Expected Key Points:**
{expected_points}

**Candidate's Answer:**
{user_answer}

**STAR Framework Evaluation:**
- **Situation:** Did they describe the context clearly?
- **Task:** Did they explain their responsibility?
- **Action:** Did they detail the specific actions they took?
- **Result:** Did they quantify the outcome?

**Scoring:**
- STAR completeness (40%)
- Relevance to question (30%)
- Specific examples (20%)
- Impact/results (10%)

**Output Format (JSON):**
```json
{{
  "score": 7.5,
  "star_analysis": {{
    "situation": "present/missing",
    "task": "present/missing",
    "action": "present/missing",
    "result": "present/missing"
  }},
  "strengths": ["point1", "point2"],
  "improvements": ["area1", "area2"],
  "feedback": "Detailed constructive feedback..."
}}
```"""

GENERATE_SUMMARY_PROMPT = """You are creating a final summary of an interview session.

**Interview Context:**
- Company: {company_name}
- Position: Based on job description
- Total Questions: {total_questions}

**Question Scores:**
{scores_summary}

**Task:** Create a comprehensive interview summary with:
1. Overall score (average of all question scores)
2. Key strengths demonstrated
3. Areas for improvement
4. Specific recommendations for the candidate

**Output Format (JSON):**
```json
{{
  "overall_score": 7.8,
  "total_questions": 7,
  "strengths": [
    "Strong technical foundation in Python",
    "Good communication skills"
  ],
  "areas_for_improvement": [
    "Could provide more specific examples",
    "Needs to work on system design concepts"
  ],
  "recommendations": [
    "Review distributed systems patterns",
    "Practice explaining complex concepts simply"
  ],
  "performance_breakdown": {{
    "technical_avg": 8.2,
    "behavioral_avg": 7.4
  }}
}}
```"""
