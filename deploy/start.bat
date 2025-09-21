@echo off
REM Chạy server trong CMD mới
start "" "D:\Git\Git\git-bash.exe" --cd="E:\job\SVYKHOA_LLM\SVYKHOA_LLM\deploy" -c "./start_server.sh"


REM Chạy tunnel trong CMD mới
start "" "D:\Git\Git\git-bash.exe" --cd="E:\job\SVYKHOA_LLM\SVYKHOA_LLM\deploy" -c "./start_tunnel.sh"


REM Đợi 5 giây để 2 script trên chạy
timeout /t 5 /nobreak >nul

REM Thực hiện git push
git add .
git commit -m "Auto commit"
git push

echo Done!
pause
