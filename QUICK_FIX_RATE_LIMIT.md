# ⚡ QUICK FIX - Rate Limit Error

## 🔴 Vấn đề

Groq `llama-3.3-70b-versatile` chỉ có **12,000 tokens/phút**. CrewAI với 3 agents vượt quá giới hạn này.

## ✅ Giải pháp đã implement

### 🎯 Solution 1: Automatic Delays (ĐÃ ACTIVE)

Code đã được update để **tự động thêm delay 20 giây** giữa các tasks:

- Task 1 (JD Analysis) → **Đợi 20s** → Task 2 (Company Research) → **Đợi 20s** → Task 3 (Questions)

**Thời gian chạy:** ~60-90 giây (thay vì 30-40 giây)

**Không cần làm gì thêm!** Chỉ cần restart backend:

```bash
./scripts/restart-be.sh
```

### 🚀 Solution 2: Switch Model (KHUYẾN NGHỊ)

Nếu vẫn muốn nhanh hơn, switch sang model có TPM cao hơn:

#### Option A: Groq Model nhỏ hơn (+67% TPM)

```bash
# Sửa file .env:
GROQ_MODEL_NAME=llama-3.1-8b-instant

# Restart:
./scripts/restart-be.sh
```

**Kết quả:** 20,000 TPM (thay vì 12,000), không cần delay!

#### Option B: Google Gemini (+2000% TPM!) 🔥

```bash
# 1. Lấy API key miễn phí: https://aistudio.google.com/apikey

# 2. Thêm vào .env:
GOOGLE_API_KEY=your_key_here
GROQ_MODEL_NAME=gemini-1.5-flash

# 3. Restart:
./scripts/restart-be.sh
```

**Kết quả:** 250,000 TPM, chạy cực nhanh, không lo rate limit!

### 🔄 Solution 3: Multiple API Keys

Nếu muốn giữ model hiện tại, thêm backup keys:

```bash
# Trong .env:
GROQ_API_KEYS_BACKUP=gsk_key2,gsk_key3
```

System sẽ tự động switch key khi gặp rate limit.

## 📊 So sánh

| Giải pháp             | Thời gian | TPM     | Chất lượng | Độ khó          |
| --------------------- | --------- | ------- | ---------- | --------------- |
| **Delays (Hiện tại)** | 60-90s    | 12k     | Cao        | ✅ Đã xong      |
| **llama-3.1-8b**      | 30-40s    | 20k     | Tốt        | ⭐ Dễ (1 dòng)  |
| **Gemini Flash**      | 20-30s    | 250k    | Rất tốt    | ⭐⭐ Trung bình |
| **Multiple Keys**     | 30-40s    | 12k x N | Cao        | ⭐⭐ Trung bình |

## 🎯 Khuyến nghị của tôi

### Cho Development:

```bash
# .env
GROQ_MODEL_NAME=llama-3.1-8b-instant
```

→ Nhanh, đủ tốt, không lo rate limit

### Cho Production:

```bash
# .env
GOOGLE_API_KEY=your_key
GROQ_MODEL_NAME=gemini-1.5-flash
```

→ Nhanh nhất, TPM cao nhất, chất lượng tốt

## 🔧 Test ngay

```bash
# 1. Restart backend
./scripts/restart-be.sh

# 2. Test với delay (solution hiện tại)
# Hoặc sửa .env và restart để dùng model khác

# 3. Check rate limit info
source venv/bin/activate
python scripts/test_rate_limit.py
```

## ❓ Câu hỏi thường gặp

**Q: Delay 20s có quá lâu không?**
A: Có thể giảm xuống 15s bằng cách sửa `delay_between_tasks=15.0` trong `service/src/api.py`

**Q: Model nào tốt nhất?**
A: `gemini-1.5-flash` - TPM cao nhất (250k), miễn phí, chất lượng tốt

**Q: Tôi có mất tiền không?**
A: KHÔNG! Tất cả các model đề xuất đều FREE

**Q: Nếu vẫn bị lỗi?**
A: Kiểm tra xem có đang chạy nhiều requests cùng lúc không. Đợi 1 phút rồi thử lại.

---

**Tóm lại:** Backend đã được fix với auto-delay. Nếu muốn nhanh hơn, switch sang `llama-3.1-8b-instant` hoặc `gemini-1.5-flash`! 🚀
