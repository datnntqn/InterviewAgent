# 🎨 Web UI Guide - AI Mock Interview Agent

## Tổng Quan

Web UI này cho phép bạn test tính năng AI Mock Interview Agent một cách trực quan, với khả năng xem kết quả từng agent theo thời gian thực.

---

## ✨ Tính Năng

### 1. **Giao Diện Hiện Đại**

- ✅ React + TailwindCSS
- ✅ Responsive design (mobile-friendly)
- ✅ Animations mượt mà
- ✅ Gradient backgrounds đẹp mắt

### 2. **Theo Dõi Agent Theo Thời Gian Thực**

- 📋 **JD Analyst**: Phân tích job description
- 🏢 **Corporate Researcher**: Nghiên cứu văn hóa công ty
- 🎯 **Lead Interviewer**: Tạo câu hỏi phỏng vấn

### 3. **Hiển Thị Kết Quả Chi Tiết**

- Mỗi agent hiển thị:
  - Trạng thái (running/completed/error)
  - Thông báo tiến trình
  - Kết quả chi tiết (JSON format)
  - Icon và màu sắc phân biệt

---

## 🚀 Cách Sử Dụng

### Bước 1: Cài Đặt Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install FastAPI and uvicorn
pip install fastapi uvicorn[standard]
```

### Bước 2: Start Server

```bash
# Sử dụng script tự động
./start_server.sh

# Hoặc start thủ công
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Bước 3: Mở Web UI

Mở trình duyệt và truy cập:

```
file:///Users/datnnt/Desktop/DatNNT/Web/Interview-Agent/web/index.html
```

Hoặc double-click vào file `web/index.html`

---

## 📱 Giao Diện

### Layout

```
┌─────────────────────────────────────────────────────────┐
│                    Header (Gradient)                    │
│         🎯 AI Mock Interview Agent                      │
└─────────────────────────────────────────────────────────┘
┌──────────────────────┬──────────────────────────────────┐
│   Input Form         │      Agent Progress              │
│                      │                                  │
│  📋 Job Description  │  📋 JD Analyst                   │
│  📄 Your CV          │     ✓ Completed                  │
│  🏢 Company Name     │     Result: {...}                │
│  🌐 Website          │                                  │
│  ⚙️  Settings        │  🏢 Corporate Researcher         │
│                      │     ⋯ Running...                 │
│  🚀 Start Button     │                                  │
│                      │  🎯 Lead Interviewer             │
│                      │     ⏳ Waiting...                │
└──────────────────────┴──────────────────────────────────┘
```

### Màu Sắc Agent

- **Running** (Đang chạy): 🔵 Blue - với typing animation
- **Completed** (Hoàn thành): 🟢 Green - với checkmark
- **Error** (Lỗi): 🔴 Red - với error message

---

## 🎯 Demo Mode

UI hiện đang chạy ở **Demo Mode** với dữ liệu giả lập để bạn test ngay:

1. Điền thông tin vào form
2. Click "Start Interview Preparation"
3. Xem các agent chạy tuần tự:
   - JD Analyst (2 giây)
   - Corporate Researcher (3 giây)
   - Lead Interviewer (4 giây)

### Chuyển Sang Real API

Để sử dụng API thật, uncomment code trong `web/index.html`:

```javascript
// Tìm dòng này trong handleSubmit function:
// Uncomment this to use real API
const response = await fetch("http://localhost:8000/api/prepare", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    job_description: jobDescription,
    user_cv: userCV,
    company_name: companyName,
    company_website: companyWebsite,
    tone,
    level,
    interview_type: interviewType,
  }),
});

const data = await response.json();
setFinalResult(data);
```

---

## 🔧 API Endpoints

### 1. Health Check

```
GET http://localhost:8000/api/health
```

### 2. Full Interview Preparation

```
POST http://localhost:8000/api/prepare
Content-Type: application/json

{
  "job_description": "...",
  "user_cv": "...",
  "company_name": "...",
  "company_website": "...",
  "tone": "friendly",
  "level": "mid",
  "interview_type": "mixed"
}
```

### 3. Quick Job Analysis

```
POST http://localhost:8000/api/quick-analysis
Content-Type: application/json

{
  "job_description": "...",
  "user_cv": "..."
}
```

### 4. Company Research Only

```
POST http://localhost:8000/api/research-company
Content-Type: application/json

{
  "company_name": "...",
  "company_website": "..."
}
```

---

## 🎨 Customization

### Thay Đổi Màu Sắc

Trong file `web/index.html`, tìm section `<style>`:

```css
.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Thay đổi màu gradient ở đây */
}
```

### Thêm Agent Mới

Trong component `AgentStatus`, thêm case mới:

```javascript
const getIcon = () => {
  switch (agent) {
    case "JD Analyst":
      return "📋";
    case "Corporate Researcher":
      return "🏢";
    case "Lead Interviewer":
      return "🎯";
    case "Your New Agent": // Thêm agent mới
      return "🤖";
    default:
      return "🤖";
  }
};
```

---

## 📊 Features Chi Tiết

### 1. Real-time Progress Tracking

- Mỗi agent hiển thị trạng thái real-time
- Typing animation khi agent đang chạy
- Smooth transitions giữa các trạng thái

### 2. Structured Results Display

- JSON formatting đẹp mắt
- Collapsible result sections
- Color-coded status indicators

### 3. Responsive Design

- Desktop: 2-column layout
- Tablet: Responsive grid
- Mobile: Single column stack

### 4. Error Handling

- Clear error messages
- Retry functionality
- Graceful degradation

---

## 🐛 Troubleshooting

### Issue: UI không load

**Solution**: Kiểm tra console trong browser (F12)

### Issue: API không kết nối được

**Solution**:

1. Kiểm tra server đang chạy: `curl http://localhost:8000/api/health`
2. Kiểm tra CORS settings trong `src/api.py`

### Issue: Agents không hiển thị

**Solution**: Kiểm tra state updates trong React DevTools

---

## 📝 Example Usage

### Ví Dụ 1: Test với Demo Data

1. Mở `web/index.html`
2. Điền thông tin:
   - Job Description: "Senior Python Developer..."
   - CV: "6 years Python experience..."
   - Company: "TechCorp"
   - Website: "https://techcorp.com"
3. Click "Start"
4. Xem agents chạy tuần tự

### Ví Dụ 2: Sử dụng Real API

1. Start server: `./start_server.sh`
2. Uncomment API code trong `index.html`
3. Reload page
4. Submit form
5. Xem kết quả thật từ CrewAI

---

## 🎯 Next Steps

1. **Thêm WebSocket** cho real-time streaming
2. **Save Results** vào database
3. **Export PDF** của interview dossier
4. **User Authentication** để lưu lịch sử
5. **Analytics Dashboard** để theo dõi usage

---

## 📞 Quick Commands

```bash
# Start server
./start_server.sh

# Install dependencies
pip install fastapi uvicorn[standard]

# Test API
curl http://localhost:8000/api/health

# View API docs
open http://localhost:8000/docs
```

---

**🎊 Enjoy your beautiful Interview Agent UI!**
