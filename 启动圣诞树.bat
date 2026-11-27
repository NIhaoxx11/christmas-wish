@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"
title 圣诞星愿

rem 优先使用 Windows 自带的 py 启动器，其次使用 python
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)

if not defined PY (
    echo 没有检测到 Python 3，将打开不需要摄像头的版本。
    echo 如需使用手势与摄像头，请先安装 Python 3: https://www.python.org/downloads/
    echo.
    start "" "圣诞星愿.html"
    timeout /t 5 >nul
    exit /b 0
)

echo 正在启动圣诞星愿的本地服务...
echo.
%PY% "server.py" "%~dp0"
echo.
echo 服务已停止，可以关闭这个窗口。
pause >nul
