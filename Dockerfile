# Base image
FROM python:3.12-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy toàn bộ project
COPY . /app

# Cho phép thực thi 2 file trong deploy/
RUN chmod +x deploy/start_server.sh deploy/start_tunnel.sh

# Cài các dependency
RUN pip install --no-cache-dir -r requirements.txt

# Mở port server (ví dụ 8000)
EXPOSE 8000

# Chạy 2 tiến trình song song (server + tunnel)
CMD ["bash", "-c", "deploy/start_server.sh & deploy/start_tunnel.sh && wait"]
