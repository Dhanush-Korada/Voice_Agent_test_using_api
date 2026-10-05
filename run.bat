@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
    if errorlevel 1 goto :error
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error

python -m pip install --upgrade pip
if errorlevel 1 goto :error
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Dhanush AI is starting. Open http://127.0.0.1:8000
python -m uvicorn server:app --host 127.0.0.1 --port 8000
goto :eof

:error
echo.
echo Setup failed. Read the error above, then check the troubleshooting section in README.md.
pause
exit /b 1