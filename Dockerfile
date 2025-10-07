# ===== BASE IMAGE =====
FROM python:3.12-slim

# ===== CÀI GÓI CẦN THIẾT =====
RUN apt-get update && apt-get install -y bash curl git && rm -rf /var/lib/apt/lists/*

# ===== THƯ MỤC LÀM VIỆC =====
WORKDIR /app

# ===== COPY TOÀN BỘ PROJECT =====
COPY . .

# ===== CÀI PYTHON LIBRARIES =====
RUN pip install --no-cache-dir -r requirements.txt

# ===== CHO PHÉP FILE SH CHẠY =====
RUN chmod +x ./deploy/start_server.sh ./deploy/start_tunnel.sh

# ===== MỞ PORT =====
EXPOSE 8000

# ===== CHẠY SERVER & TUNNEL =====
CMD ["bash", "-c", "cd deploy && ./start_server.sh & ./start_tunnel.sh && wait"]
