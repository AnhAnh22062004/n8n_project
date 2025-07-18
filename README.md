===============================
🖼️ Add Text to Image API (Flask + Docker)
===============================

-------------------------------------
🗂️ Cấu trúc thư mục dự án
-------------------------------------

n8n_project/
├── app.py              # Flask app xử lý ảnh
├── Dockerfile          # Docker cấu hình
├── requirements.txt    # Các thư viện Python cần thiết
└── temp_images/        # Thư mục lưu ảnh sau xử lý

-------------------------------------
🐳 1. Build Docker Image
-------------------------------------

docker build -t add-text-api .

-------------------------------------
▶️ 2. Run Docker Container
-------------------------------------

docker run -d \
  -p 5000:5000 \
  --name add-text-api \
  -v $(pwd)/temp_images:/home/n8nuser/n8n_project/temp_images \
  add-text-api

-------------------------------------
✅ 3. Gọi API từ n8n hoặc Postman
-------------------------------------

Phương thức: POST
Endpoint: http://<your-ip>:5000/add-text
Content-Type: multipart/form-data


- file         : Ảnh cần xử lý (file upload)
- text         : Nội dung muốn chèn vào ảnh
- font_size    : (tuỳ chọn) kích thước chữ, mặc định 30
- position_y   : (tuỳ chọn) toạ độ Y để vẽ text, mặc định = 90% chiều cao ảnh
- color        : (tuỳ chọn) mã màu hex, ví dụ #2b00ff
- font_path    : (tuỳ chọn) đường dẫn tới font TTF, ví dụ /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf


-------------------------------------
📦 requirements.txt
-------------------------------------

Flask==2.3.3
Pillow==10.3.0

-------------------------------------
📄 Dockerfile mẫu
-------------------------------------

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]

