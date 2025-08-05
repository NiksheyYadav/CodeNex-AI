@echo off
setlocal enabledelayedexpansion

echo Starting FastAPI server with direct output...
echo Python version:
python --version
echo.

echo Running FastAPI server...
python -c "import sys; print('Python executable:', sys.executable); import uvicorn; print('Uvicorn version:', uvicorn.__version__); uvicorn.run('ui.server:app', host='0.0.0.0', port=8000, reload=True)" 2>&1 | tee fastapi_output.log

echo Server stopped.
pause
