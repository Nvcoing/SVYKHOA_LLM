# # run
# chmod +x deploy.sh
# ./deploy.sh
# Chạy uvicorn ở nền
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > llmserver.log 2>&1 &
echo "🚀 LLM Server đang chạy trên cổng 8000..."

# Đợi 3s cho server khởi động
sleep 3

# Chạy Cloudflare Tunnel để public API
nohup cloudflared tunnel --url http://localhost:8000 > cloudflare.log 2>&1 &
echo "🌍 Cloudflare Tunnel đang chạy, xem log tại cloudflare.log"
echo "👉 Truy cập endpoint public trong log Cloudflare."