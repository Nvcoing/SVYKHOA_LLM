#!/bin/bash
# chmod +x start_server.sh
# ./start_server.sh

set -e

echo "Obfuscating HTML..."
html-obfuscator chatsvy.html > index.html

echo "Khởi động Uvicorn server tại http://127.0.0.1:8000 ..."
uvicorn main:app --reload
