@echo off
REM Chạy server trong CMD mới
start "" cmd /k "bash start_server.sh"

REM Chạy tunnel trong CMD mới
start "" cmd /k "bash start_tunnel.sh"

REM Đợi 5 giây để 2 script trên chạy
timeout /t 5 /nobreak >nul

REM Thực hiện git push
git add .
git commit -m "Auto commit"
git push

echo Done!
pause
