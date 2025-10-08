# Healthcare Chatbot FastAPI

## Mô tả
Ứng dụng chatbot y tế được chuyển đổi từ Flask sang FastAPI, hỗ trợ 3 chuyên khoa:
- GDM (Gestational Diabetes Mellitus - Tiểu đường thai kỳ)
- CKD (Chronic Kidney Disease - Bệnh thận mãn tính)
- PPD (Postpartum Depression - Trầm cảm sau sinh)

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```bash
# Cách 1: Sử dụng script
python run_fastapi.py

# Cách 2: Sử dụng uvicorn trực tiếp
uvicorn app:app --host 0.0.0.0 --port 5012 --reload

# Cách 3: Chạy file app.py trực tiếp
python app.py
```

## API Endpoints

### Web Interface
- `GET /` - Trang chọn chuyên khoa
- `GET /chat` - Trang chat với chatbot

### API Endpoints
- `POST /ask` - Gửi câu hỏi và nhận câu trả lời
  - Parameters:
    - `question` (required): Câu hỏi của người dùng
    - `role` (optional): "doctor" hoặc "unknown" (default: "unknown")
    - `model_type` (optional): "gdm", "ckd", hoặc "ppd" (default: "gdm")
    - `responseWithAudio` (optional): "true" hoặc "false" (default: "false")

- `POST /upload` - Upload file âm thanh để chuyển đổi thành văn bản
  - File upload: `audio` field

## Thay đổi từ Flask sang FastAPI

### Cải tiến chính:
1. **Type hints**: Sử dụng type hints cho tất cả parameters
2. **Async/await**: Hỗ trợ async operations tốt hơn
3. **Automatic API documentation**: Truy cập `/docs` để xem Swagger UI
4. **Request validation**: Tự động validate request parameters
5. **Performance**: Hiệu suất tốt hơn Flask

### Breaking changes:
- URL paths giữ nguyên
- Response format giữ nguyên
- Form data handling thay đổi (sử dụng `Form()` thay vì `request.form`)
- File upload handling thay đổi (sử dụng `UploadFile` thay vì `request.files`)

## Truy cập ứng dụng
- Web interface: http://localhost:5012/
- API documentation: http://localhost:5012/docs
- Alternative API docs: http://localhost:5012/redoc