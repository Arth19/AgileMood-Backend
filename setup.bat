@echo off
cd /d %~dp0

if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Updating pip...
python -m pip install --upgrade pip setuptools wheel

echo Installing dependencies...
if exist requirements.txt (
    pip install --no-cache-dir -r requirements.txt
)

echo Fixing potential Pydantic issues...
pip uninstall -y pydantic
pip install --no-cache-dir pydantic