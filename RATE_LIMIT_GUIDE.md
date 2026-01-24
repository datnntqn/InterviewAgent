# 🚀 Rate Limit Handling Guide

## Vấn đề Rate Limit với Groq API

Groq's `llama-3.3-70b-versatile` có giới hạn:

- **12,000 tokens/phút (TPM)**
- **30 requests/phút (RPM)**

Khi CrewAI chạy 3 agents liên tiếp, tổng token usage có thể vượt quá giới hạn này.

## ✅ Giải pháp đã implement

### 1. **Automatic Retry với Exponential Backoff**

Code tự động retry khi gặp rate limit error với delay tăng dần:

- Attempt 1: 16s (theo gợi ý của Groq)
- Attempt 2: 32s
- Attempt 3: 60s (max)

### 2. **API Key Rotation**

Nếu bạn có nhiều Groq API keys, hệ thống sẽ tự động switch qua key khác khi gặp rate limit.

### 3. **Alternative Model Recommendations**

Các model free khác có rate limit cao hơn:

| Model                  | Provider         | TPM     | RPM | Đặc điểm                     |
| ---------------------- | ---------------- | ------- | --- | ---------------------------- |
| `llama-3.1-8b-instant` | Groq             | 20,000  | 30  | Nhanh hơn, limit cao hơn 67% |
| `gemini-1.5-flash`     | Google AI Studio | 250,000 | 5   | TPM cao nhất (FREE!)         |
| `deepseek-v3`          | OpenRouter       | 50,000  | 20  | Chất lượng tốt, balanced     |
| `qwen-3-8b`            | SiliconFlow      | 30,000  | 30  | Nhanh, multilingual          |

## 📝 Cách sử dụng

### Option 1: Single API Key (Hiện tại)

Giữ nguyên `.env`:

```bash
GROQ_API_KEY=your_primary_key_here
```

Code sẽ tự động retry khi gặp rate limit.

### Option 2: Multiple API Keys (Khuyến nghị)

Thêm backup keys vào `.env`:

```bash
# Primary key
GROQ_API_KEY=gsk_primary_key_here

# Backup keys (comma-separated)
GROQ_API_KEYS_BACKUP=gsk_backup_key_1,gsk_backup_key_2,gsk_backup_key_3
```

Hệ thống sẽ tự động rotate qua các keys khi gặp rate limit.

### Option 3: Sử dụng Model khác

#### Groq - Model nhỏ hơn (Dễ nhất)

```python
# Trong src/config.py, thay đổi default model:
groq_model_name: str = Field(
    default_factory=lambda: os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
)
```

Hoặc trong `.env`:

```bash
GROQ_MODEL_NAME=llama-3.1-8b-instant
```

#### Google Gemini (TPM cao nhất - 250k!)

```bash
# .env
GOOGLE_API_KEY=your_google_api_key
GROQ_MODEL_NAME=gemini-1.5-flash
```

Lấy API key miễn phí tại: https://aistudio.google.com/apikey

## 🔧 Cách integrate vào code hiện tại

### Cách 1: Sử dụng wrapper (Khuyến nghị)

Thay đổi trong `service/src/api.py`:

```python
# Thay vì:
from src.crews.interview_crew import prepare_for_interview

# Dùng:
from src.utils import prepare_interview_with_retry

# Trong endpoint:
@app.post("/api/prepare")
async def prepare_interview(request: PrepareRequest):
    result = prepare_interview_with_retry(  # Thay vì prepare_for_interview
        job_description=request.job_description,
        user_cv=request.user_cv,
        company_name=request.company_name,
        company_website=request.company_website,
        tone=request.tone,
        level=request.level,
        interview_type=request.interview_type
    )
    return {"status": "success", "result": result}
```

### Cách 2: Manual retry trong API endpoint

```python
from src.utils import RateLimitHandler, with_rate_limit_retry

@app.post("/api/prepare")
@with_rate_limit_retry(rotate_keys=True)
async def prepare_interview(request: PrepareRequest):
    # Code hiện tại của bạn
    result = prepare_for_interview(...)
    return {"status": "success", "result": result}
```

## 🎯 Khuyến nghị

### Ngắn hạn (Dùng ngay):

1. **Thêm 2-3 Groq API keys** vào `.env` để rotate
2. **Sử dụng wrapper** `prepare_interview_with_retry` trong API

### Trung hạn (Nếu vẫn gặp vấn đề):

1. **Switch sang `llama-3.1-8b-instant`** (Groq, TPM cao hơn 67%)
2. Hoặc **Google Gemini 1.5 Flash** (TPM cao nhất: 250k!)

### Dài hạn (Production):

1. Implement **request queuing** với Celery/Redis
2. **Rate limiting** ở application level
3. Sử dụng **paid tier** của Groq (unlimited)

## 📊 So sánh Models Free

### Chất lượng cao, TPM thấp:

- ✅ `llama-3.3-70b-versatile` (Groq) - 12k TPM - **Hiện tại**
- ✅ `deepseek-v3` (OpenRouter) - 50k TPM - Tốt cho reasoning

### Balanced:

- ✅ `gemini-1.5-flash` (Google) - 250k TPM - **Khuyến nghị nhất!**
- ✅ `llama-3.1-8b-instant` (Groq) - 20k TPM - Dễ switch

### Nhanh, TPM cao:

- ✅ `qwen-3-8b` (SiliconFlow) - 30k TPM
- ✅ `gemma-3-27b-it` (Google) - 15k TPM

## 🔗 Links hữu ích

- Groq Console: https://console.groq.com/keys
- Google AI Studio: https://aistudio.google.com/apikey
- OpenRouter: https://openrouter.ai/keys
- Rate Limits Comparison: https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json

## ❓ FAQ

**Q: Tôi nên dùng bao nhiêu API keys?**
A: 2-3 keys là đủ. Groq cho phép tạo nhiều keys miễn phí.

**Q: Model nào tốt nhất cho use case này?**
A: `gemini-1.5-flash` (Google) - TPM cao nhất (250k), chất lượng tốt, hoàn toàn miễn phí.

**Q: Tôi có cần thay đổi code nhiều không?**
A: Không, chỉ cần thay 1 dòng import trong `api.py` là xong.

**Q: Retry có ảnh hưởng đến user experience không?**
A: Có thể delay 16-60s. Nên hiển thị loading indicator cho user.

## 🚀 Quick Start

1. **Thêm backup keys vào `.env`:**

```bash
GROQ_API_KEYS_BACKUP=key2,key3
```

2. **Update import trong `service/src/api.py`:**

```python
from src.utils import prepare_interview_with_retry
```

3. **Thay function call:**

```python
result = prepare_interview_with_retry(...)  # Thay vì prepare_for_interview
```

4. **Restart backend:**

```bash
./scripts/restart-be.sh
```

Done! ✅
