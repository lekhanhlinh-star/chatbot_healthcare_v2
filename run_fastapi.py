#!/usr/bin/env python3
"""
Script để chạy ứng dụng FastAPI Healthcare Chatbot
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5012, reload=True, debug=True)