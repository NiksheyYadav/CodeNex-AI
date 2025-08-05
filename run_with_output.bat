@echo off
echo Starting script with output capture...
python run_server.py > output.log 2>&1
type output.log
pause
