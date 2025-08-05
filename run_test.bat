@echo off
echo Running test script...
python test_output.py > test_output.log 2>&1
type test_output.log
pause
