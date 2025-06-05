@echo off
echo Starting Python backend...

REM Move to this directory
cd /d "%~dp0"

REM Confirm current path and check file presence
echo Current directory: %cd%
dir App.py

REM Run the backend
python "App.py"

pause
