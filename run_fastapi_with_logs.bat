@echo off
setlocal enabledelayedexpansion

:: Redirect all output to a log file
echo Starting FastAPI server with full logging... > fastapi_full_log.txt 2>&1
echo Python version: >> fastapi_full_log.txt 2>&1
python --version >> fastapi_full_log.txt 2>&1
echo. >> fastapi_full_log.txt 2>&1

echo Running FastAPI server... >> fastapi_full_log.txt 2>&1

:: Run Python with unbuffered output and redirect all output to the log file
python -u -c "
import sys
import os
import traceback

print('Python executable:', sys.executable)
print('Python version:', sys.version)
print('Current working directory:', os.getcwd())
print('Environment variables:')
for k, v in os.environ.items():
    if 'PYTHON' in k or 'PATH' in k:
        print(f'  {k}: {v}')

print('\nTrying to import FastAPI and Uvicorn...')
try:
    import fastapi
    import uvicorn
    print(f'Successfully imported FastAPI {fastapi.__version__} and Uvicorn {uvicorn.__version__}')
    
    print('\nCreating FastAPI app...')
    app = fastapi.FastAPI()
    
    @app.get('/')
    async def root():
        return {'message': 'Hello from FastAPI!'}
    
    print('Starting Uvicorn server...')
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
    
except Exception as e:
    print(f'\nError: {e}', file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    input('Press Enter to exit...')
" >> fastapi_full_log.txt 2>&1

echo Server stopped. Check fastapi_full_log.txt for details.
pause
