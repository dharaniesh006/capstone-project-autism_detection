@echo off
setlocal

echo ==========================================
echo    Autism Detection Project Setup
echo ==========================================

:: Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

:: Upgrade pip and install requirements
echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements from requirements.txt...
pip install -r requirements.txt

:menu
cls
echo ==========================================
echo    Autism Detection Project Runner
echo ==========================================
echo 1. Run Django Web Application
echo 2. Run Streamlit Visualization Tool
echo 3. Exit
echo ==========================================
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Django Web Application...
    echo Note: Ensure your local MySQL server is running.
    cd webapp
    python manage.py runserver
    cd ..
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Starting Streamlit Visualization Tool...
    cd streamlit_app
    streamlit run app.py
    cd ..
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Exiting...
    exit /b
)

echo Invalid choice, please try again.
pause
goto menu
