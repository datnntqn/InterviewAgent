# 📋 Tài Liệu Yêu Cầu Hệ Thống: AI Mock Interview Agent

## 1. Tổng quan dự án
Xây dựng một AI Agent hỗ trợ người dùng luyện tập phỏng vấn cá nhân hóa bằng cách kết hợp dữ liệu từ CV cá nhân (Reactive Resume), yêu cầu công việc (JD) và bối cảnh văn hóa doanh nghiệp.

## 2. Các thành phần đầu vào (Input)
* **CV (User Profile):** File JSON được xuất từ [Reactive Resume](https://rxresu.me/).
* **Job Description (JD):** Nội dung mô tả công việc người dùng dán vào chatbox.
* **Company URL:** Đường dẫn website công ty để thu thập thông tin bối cảnh.

## 3. Quy trình xử lý dữ liệu (Pipeline)
1.  **Parsing:** LLM phân tích JD để trích xuất Technical Keywords, Years of Experience và Required Skills.
2.  **Crawling:** Sử dụng **Playwright** quét Website công ty (trang chủ, trang tuyển dụng, trang giới thiệu) để lấy thông tin về văn hóa, giá trị cốt lõi và các dự án tiêu biểu.
3.  **Synthesis:** Kết hợp thông tin từ CV, JD và Website để tạo ra bộ câu hỏi phỏng vấn "đo ni đóng giày" cho từng người dùng.

---

## 4. Tính năng cốt lõi (Core Features)

### 4.1. Tùy chỉnh mức độ và Phong cách (Interview Persona)
Cho phép người dùng thiết lập môi trường phỏng vấn giả lập:
* **Mức độ khó (Level):** Intern, Junior, Senior, hoặc Lead/Manager. AI sẽ điều chỉnh độ sâu của các câu hỏi kỹ thuật theo level này.
* **Phong cách phỏng vấn (Tone):** * *Thân thiện:* Khuyến khích, gợi mở.
    * *Khó tính:* Tập trung vào chi tiết nhỏ, bắt bẻ logic.
    * *Áp lực (Stress Interview):* Đưa ra các tình huống dồn dập, thách thức quan điểm của ứng viên.

### 4.2. Phân tách Section Phỏng vấn
Người dùng có quyền chọn bắt đầu với một trong hai phần:
* **Kỹ năng (Technical Skills):** Tập trung vào kiến thức chuyên môn dựa trên JD và các project trong CV.
* **Văn hóa (Culture Fit):** Tập trung vào hành vi và thái độ. AI sẽ hướng dẫn người dùng trả lời theo mô hình **STAR** (Situation, Task, Action, Result).

### 4.3. Hệ thống ghi nhớ và Đào sâu (Contextual Memory)
AI không chỉ hỏi các câu rời rạc mà có khả năng:
* Lưu trữ nội dung các câu trả lời trước đó trong phiên chat.
* Đặt các câu hỏi đào sâu (**Follow-up questions**) dựa trên ý người dùng vừa trả lời (ví dụ: "Bạn vừa nói có sử dụng Redis, vậy bạn đã xử lý vấn đề Cache Aside như thế nào trong dự án đó?").

### 4.4. Đánh giá và Chấm điểm (Scoring System)
Sau mỗi câu trả lời hoặc khi kết thúc buổi phỏng vấn:
* **Chấm điểm:** Đưa ra thang điểm (ví dụ: 8/10) dựa trên mức độ hoàn thiện và sự phù hợp.
* **Nhận xét:** Chỉ ra điểm mạnh và điểm cần cải thiện.
* **Câu trả lời mẫu:** Cung cấp một phiên bản "Câu trả lời tốt nhất" (Best Practice) để người dùng tham khảo và học hỏi.

---

## 5. Luồng tương tác (User Flow)
1. User tải lên JSON CV -> Dán JD -> Cung cấp Link Website.
2. User chọn **Level** và **Phong cách** phỏng vấn.
3. User chọn **Section** muốn bắt đầu (Technical hoặc Culture).
4. AI đặt câu hỏi -> User trả lời -> AI nhận xét + chấm điểm -> AI hỏi "Bạn có muốn cải thiện câu trả lời này hay chuyển sang câu tiếp theo?".
5. Kết thúc buổi phỏng vấn: AI tổng hợp báo cáo đánh giá cuối cùng.