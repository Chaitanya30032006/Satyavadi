@echo off
echo Starting TruthGuard Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo.
echo Starting Flask server...
echo Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop the server
echo.
python app.py

pause

