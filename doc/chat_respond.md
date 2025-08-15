# 4 Loại phản hồi của Chatbot

## A. Chuẩn đoán bệnh
- **Mục tiêu**: Cung cấp thông tin y khoa chính xác, kèm tài liệu tham khảo để hỗ trợ bác sĩ trẻ.  
- **Giải quyết vấn đề**: Giúp người dùng xác định tình trạng bệnh và biết hướng điều trị dựa trên triệu chứng.

## B. Trả lời tự nhiên (Chào hỏi)
- **Mục tiêu**: Tạo thiện cảm, kết nối ban đầu và giới thiệu khả năng của chatbot.  
- **Giải quyết vấn đề**: Giúp người dùng cảm thấy thoải mái khi bắt đầu trò chuyện, giảm rào cản giao tiếp.

## C. Xử lý câu hỏi mơ hồ
- **Mục tiêu**: Đảm bảo bot không trả lời sai hoặc lệch chủ đề khi thông tin chưa đủ.  
- **Giải quyết vấn đề**: Yêu cầu người dùng cung cấp thông tin bổ sung để có câu trả lời chính xác hơn.

## D. Tư vấn
- **Mục tiêu**: Đưa ra lời khuyên chuyên môn và gợi ý tài liệu, khóa học liên quan.  
- **Giải quyết vấn đề**: Giúp người dùng cải thiện kỹ năng, nắm rõ cách xử lý tình huống trong thực tế.

```mermaid
flowchart TB
    U[Người dùng gửi câu hỏi] --> N{Phân loại câu hỏi}

    N -->|A: Chuẩn đoán bệnh| A1[Trả lời chẩn đoán]
    A1 --> A2[**Mục tiêu:** Cung cấp thông tin y khoa chính xác]
    A1 --> A3[**Giải quyết:** Giúp xác định tình trạng bệnh & hướng điều trị]

    N -->|B: Trả lời tự nhiên| B1[Trả lời chào hỏi]
    B1 --> B2[**Mục tiêu:** Tạo thiện cảm & kết nối ban đầu]
    B1 --> B3[**Giải quyết:** Giúp người dùng thoải mái trò chuyện]

    N -->|C: Câu hỏi mơ hồ| C1[Yêu cầu làm rõ]
    C1 --> C2[**Mục tiêu:** Tránh trả lời sai khi thiếu dữ liệu]
    C1 --> C3[**Giải quyết:** Thu thập thêm thông tin từ người dùng]

    N -->|D: Tư vấn| D1[Trả lời tư vấn]
    D1 --> D2[**Mục tiêu:** Cung cấp lời khuyên + tài liệu]
    D1 --> D3[**Giải quyết:** Giúp cải thiện kỹ năng & xử lý thực tế]
