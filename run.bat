@echo off
echo Checking virtual environment...

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Starting server...
python src\server.py

pause
