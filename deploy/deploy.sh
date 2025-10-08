#!/bin/bash
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
# Chạy server trong nền và auto reload
nohup bash ./start_server.sh > server.log 2>&1 &

# Chạy tunnel trong nền
nohup bash ./start_tunnel.sh > tunnel.log 2>&1 &

echo "Đã khởi động cả server và tunnel trong nền!"
echo "Xem log bằng: tail -f server.log hoặc tail -f tunnel.log"
