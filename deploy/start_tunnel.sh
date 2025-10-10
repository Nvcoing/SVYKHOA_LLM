#!/bin/bash
# chmod +x start_tunnel.sh
# ./start_tunnel.sh

set -e

LOCAL_URL="http://127.0.0.1:8000"
OUTPUT_FILE="public_api"

echo "🚀 Khởi động Cloudflare Tunnel cho $LOCAL_URL ..."

# Xoá file cũ nếu có
rm -f $OUTPUT_FILE

# Chạy cloudflared 1 lần, bắt dòng có URL rồi kill process
cloudflared tunnel --url $LOCAL_URL 2>&1 | while read line; do
    echo "$line"
    if [[ "$line" =~ https://[a-z0-9.-]+\.trycloudflare\.com ]]; then
        PUBLIC_URL="${BASH_REMATCH[0]}"
        echo "Public API: $PUBLIC_URL"
        echo "$PUBLIC_URL" > $OUTPUT_FILE
        echo "Đã lưu vào $OUTPUT_FILE"
        # pkill -P $$ cloudflared   # Kill process con cloudflared
        # exit 0
    fi
done
