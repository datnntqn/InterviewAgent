# 🎯 Hướng Dẫn Sử Dụng UI với Real CrewAI

## ✅ Đã Cập Nhật!

UI giờ đã kết nối **THẬT** với CrewAI và Llama 3 LLM! Bạn sẽ thấy kết quả thực từ từng agent.

---

## 🚀 Cách Chạy

### Bước 1: Đảm Bảo Ollama Đang Chạy

```bash
# Kiểm tra Ollama
curl http://localhost:11434/api/tags

# Nếu chưa chạy, start Ollama
docker-compose up ollama -d

# Pull Llama 3 model (nếu chưa có)
docker-compose exec ollama ollama pull llama3
```

### Bước 2: Start API Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
./start_server.sh

# Hoặc start thủ công
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Bạn sẽ thấy:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Bước 3: Mở UI

```bash
open web/index.html
```

Hoặc truy cập: `file:///Users/datnnt/Desktop/DatNNT/Web/Interview-Agent/web/index.html`

---

## 🎨 Giao Diện Mới

### Server Status Indicator

- 🟢 **Online** - Server đang chạy, sẵn sàng
- 🔴 **Offline** - Cần start server
- 🟡 **Checking** - Đang kiểm tra

### Real-time Agent Progress

Khi bạn click "Start", bạn sẽ thấy:

1. **📋 JD Analyst** (Agent 1)

   - Status: Running → Completed
   - Message: "Analyzing job description..."
   - Result: Kết quả THẬT từ Llama 3

2. **🏢 Corporate Researcher** (Agent 2)

   - Status: Running → Completed
   - Message: "Scraping company website..."
   - Result: Dữ liệu THẬT từ web scraping

3. **🎯 Lead Interviewer** (Agent 3)
   - Status: Running → Completed
   - Message: "Generating interview questions..."
   - Result: Câu hỏi THẬT được tạo bởi LLM

---

## 🔄 Luồng Hoạt Động

```
1. User điền form và click "Start"
   ↓
2. UI gửi request đến API (http://localhost:8000/api/prepare-stream)
   ↓
3. API tạo 3 agents với CrewAI
   ↓
4. Agent 1 (JD Analyst) chạy với Llama 3
   → Stream kết quả về UI
   ↓
5. Agent 2 (Corporate Researcher) chạy
   → Scrape website thật
   → Stream kết quả về UI
   ↓
6. Agent 3 (Lead Interviewer) chạy
   → Tổng hợp và tạo câu hỏi
   → Stream kết quả về UI
   ↓
7. ✅ Hoàn thành!
```

---

## 📊 Ví Dụ Kết Quả Thật

### JD Analyst Output:

```
Based on the job description analysis:

Skills Required:
- Python (5+ years)
- Django/Flask
- PostgreSQL
- Docker & Kubernetes
- RESTful API design
- CI/CD pipelines

Experience Level: Senior (5+ years)

Skill Gaps:
- Kubernetes experience not mentioned in CV
- CI/CD pipeline design needs more detail

Strengths:
- Strong Python background (6 years)
- Django and Flask proficiency
- PostgreSQL experience
- Docker knowledge
```

### Corporate Researcher Output:

```
Company Culture Analysis for TechCorp:

Mission: "Building innovative solutions for tomorrow's challenges"

Core Values:
1. Innovation - Embrace new technologies
2. Collaboration - Team-first approach
3. Excellence - High quality standards
4. Continuous Learning

Work Environment:
- Remote-friendly culture
- Focus on work-life balance
- Regular hackathons and learning sessions

Recent Projects:
- Cloud migration initiative
- AI/ML integration
- Microservices architecture
```

### Lead Interviewer Output:

```
Interview Preparation Dossier:

TECHNICAL QUESTIONS:
1. Describe your experience building RESTful APIs with Django
2. How would you optimize PostgreSQL queries for large datasets?
3. Explain your approach to containerizing Python applications with Docker
4. What's your experience with CI/CD pipelines?

BEHAVIORAL QUESTIONS (STAR Method):
1. Tell me about a time you had to learn a new technology quickly
   - Situation: What was the context?
   - Task: What did you need to accomplish?
   - Action: What steps did you take?
   - Result: What was the outcome?

2. Describe a situation where you improved team collaboration
   [STAR framework]

COMPANY-SPECIFIC QUESTIONS:
1. How do you align with our value of continuous learning?
2. What interests you about our cloud migration initiative?

STRATEGY:
- Emphasize your 6 years of Python experience
- Prepare examples of Docker usage
- Research Kubernetes basics to address gap
- Highlight collaborative projects
- Show enthusiasm for innovation
```

---

## ⚙️ API Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/api/health
```

### 2. Streaming Interview Preparation

```bash
curl -X POST http://localhost:8000/api/prepare-stream \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "...",
    "user_cv": "...",
    "company_name": "TechCorp",
    "company_website": "https://techcorp.com",
    "tone": "friendly",
    "level": "senior",
    "interview_type": "mixed"
  }'
```

### 3. API Documentation

Truy cập: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Issue: Server Status "Offline"

**Giải pháp:**

```bash
# 1. Kiểm tra server đang chạy
ps aux | grep uvicorn

# 2. Kiểm tra port 8000
lsof -i :8000

# 3. Start lại server
./start_server.sh
```

### Issue: "Connection refused"

**Giải pháp:**

```bash
# Kiểm tra Ollama
curl http://localhost:11434/api/tags

# Start Ollama nếu cần
docker-compose up ollama -d
```

### Issue: Agents không hiển thị kết quả

**Giải pháp:**

1. Mở Browser Console (F12)
2. Kiểm tra Network tab
3. Xem có lỗi CORS không
4. Kiểm tra server logs

### Issue: Kết quả quá lâu

**Lý do:** LLM đang xử lý thật, mất thời gian

- JD Analyst: ~30-60 giây
- Corporate Researcher: ~20-40 giây (tùy website)
- Lead Interviewer: ~40-80 giây

**Tổng thời gian:** ~2-3 phút cho toàn bộ workflow

---

## 💡 Tips

### 1. Test Nhanh

Dùng job description và CV ngắn gọn để test nhanh hơn

### 2. Xem Logs

```bash
# Terminal chạy server sẽ hiển thị logs real-time
# Bạn sẽ thấy:
# - Agent đang chạy
# - LLM responses
# - Errors (nếu có)
```

### 3. Multiple Tests

Server hỗ trợ multiple requests, nhưng chạy tuần tự để tránh quá tải Ollama

---

## 🎯 So Sánh Demo vs Real

| Feature          | Demo Mode | Real Mode            |
| ---------------- | --------- | -------------------- |
| **Tốc độ**       | 9 giây    | 2-3 phút             |
| **Kết quả**      | Giả lập   | Thật từ LLM          |
| **Web Scraping** | Fake data | Thật từ website      |
| **Câu hỏi**      | Cố định   | Tùy chỉnh theo input |
| **Server**       | Không cần | Cần chạy             |

---

## 📝 Example Test Data

### Job Description:

```
Senior Python Developer

Requirements:
- 5+ years Python experience
- Django or Flask framework
- PostgreSQL database
- Docker containerization
- RESTful API design
- CI/CD experience

Nice to have:
- Kubernetes
- AWS/GCP
- React
```

### Your CV:

```
John Doe - Software Engineer

Experience: 6 years Python development
Skills: Python, Django, Flask, PostgreSQL, Docker, Git, REST APIs

Projects:
- Built microservices with Django
- Designed RESTful APIs
- Worked with PostgreSQL optimization
- Some Docker experience
```

### Company:

- Name: TechCorp
- Website: https://www.example.com (hoặc bất kỳ website thật nào)

---

## 🎊 Kết Luận

Bây giờ bạn có một **UI hoàn chỉnh** kết nối với **CrewAI thật**!

✅ Real-time streaming  
✅ Kết quả từ Llama 3 LLM  
✅ Web scraping thật  
✅ Câu hỏi được tạo tự động  
✅ STAR method integration

**Chúc bạn test vui vẻ! 🚀**
