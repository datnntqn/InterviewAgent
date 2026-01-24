# AI Interview Coach - Streamlit Client

## Tổng Quan

Dashboard Streamlit với 2 chế độ:

1. **📋 Report Mode**: Xem tất cả câu hỏi và chiến lược (static)
2. **🎤 Interactive Interview**: Phỏng vấn thực tế với đánh giá real-time

## Cài Đặt

```bash
# Install dependencies
pip install streamlit requests

# Or from requirements.txt
pip install -r requirements.txt
```

## Chạy Ứng Dụng

```bash
# Start backend first
./scripts/start_server_new.sh

# Then start Streamlit (in another terminal)
./scripts/start_streamlit.sh
```

## Sử Dụng

### Bước 1: Chuẩn Bị Interview

1. Điền thông tin vào sidebar:
   - Job Description
   - Your CV
   - Company Name
   - Company Website
   - Tone (Friendly/Strict)
   - Level (Junior/Mid/Senior)

2. Click **"🚀 Start Interview Analysis"**

3. Đợi CrewAI phân tích (30-60 giây)

### Bước 2: Chọn Mode

#### 📋 Report Mode

- Xem tất cả câu hỏi được tạo
- Review chiến lược phỏng vấn
- Ghi chú câu trả lời
- Không có đánh giá real-time

#### 🎤 Interactive Interview Mode

- Phỏng vấn từng câu một
- Trả lời và nhận feedback ngay lập tức
- Xem điểm số cho mỗi câu trả lời
- Nhận tổng kết cuối cùng

### Interactive Mode Workflow

```
1. Click "🎬 Start Interactive Interview"
   ↓
2. Đọc câu hỏi
   ↓
3. Nhập câu trả lời
   ↓
4. Click "📤 Submit Answer"
   ↓
5. Xem feedback và điểm số
   ↓
6. Tiếp tục với câu hỏi tiếp theo
   ↓
7. Xem tổng kết cuối cùng
```

## Tính Năng

### Report Mode

- ✅ Chiến lược phỏng vấn
- ✅ Roadmap chuẩn bị
- ✅ Key talking points
- ✅ Câu hỏi technical
- ✅ Câu hỏi behavioral (STAR)
- ✅ Câu hỏi về công ty

### Interactive Mode

- ✅ Q&A real-time
- ✅ Đánh giá tức thì (LLM-powered)
- ✅ Điểm số 0-10 cho mỗi câu
- ✅ Feedback chi tiết
- ✅ Strengths & improvements
- ✅ Progress tracking
- ✅ Interview history
- ✅ Final summary

## Cấu Trúc File

```
client/
├── app.py                  # Main Streamlit app
├── interactive_mode.py     # Interactive interview component
├── config.py              # Configuration & mock data
├── styles.py              # CSS styles
├── utils.py               # Utility functions
└── README.md              # This file
```

## Session State

Streamlit sử dụng session state để lưu:

- `analysis_result`: Kết quả từ CrewAI
- `interview_thread_id`: LangGraph session ID
- `interview_active`: Trạng thái phỏng vấn
- `current_question`: Câu hỏi hiện tại
- `interview_progress`: Tiến độ (current/total)
- `interview_history`: Lịch sử Q&A

## API Integration

### CrewAI (Report Generation)

```python
POST /api/prepare
→ Returns: technical_questions, behavioral_questions, strategy
```

### LangGraph (Interactive Interview)

```python
# Start
POST /api/interview/start
→ Returns: thread_id, first_question

# Submit answer
POST /api/interview/chat/{thread_id}
→ Returns: feedback, next_question, progress

# Get summary
GET /api/interview/summary/{thread_id}
→ Returns: overall_score, strengths, improvements
```

## Troubleshooting

### "Connection refused"

- Backend chưa chạy
- Run: `./scripts/start_server_new.sh`

### "Please run interview preparation first"

- Chưa generate questions
- Click "🚀 Start Interview Analysis" trong sidebar

### Interactive mode không hiển thị

- Chưa có `analysis_result`
- Chạy Report Mode trước

### Session expired

- Server restart sẽ xóa sessions
- Start lại interview

## Tips

1. **Mock Data**: Click "📝 Fill Mock Data" để test nhanh
2. **Progress**: Theo dõi progress bar trong Interactive Mode
3. **History**: Xem lại tất cả câu hỏi và feedback
4. **End Early**: Click "🛑 End Interview" nếu muốn dừng sớm

## Screenshots

### Report Mode

- Tabs: Strategy, Technical, Behavioral, Company Fit
- Static view của tất cả câu hỏi

### Interactive Mode

- Progress bar
- Current question
- Answer input
- Real-time feedback
- Interview history
- Final summary

## Next Steps

- [ ] Add voice input/output
- [ ] Save interview sessions
- [ ] Export results to PDF
- [ ] Multi-language support
- [ ] Video interview simulation

---

**Enjoy your AI-powered interview preparation!** 🚀
