@echo off
REM Build script for n8n Workflow Generator (Windows)
REM This script builds both the TypeScript and Python components

setlocal enabledelayedexpansion

echo 🚀 Starting build process for n8n Workflow Generator...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js to continue.
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python to continue.
    exit /b 1
)

REM Create build directories
echo [INFO] Creating build directories...
if not exist "dist" mkdir dist
if not exist "static\js" mkdir static\js
if not exist "static\css" mkdir static\css
if not exist "templates" mkdir templates

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
if exist "package.json" (
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install Node.js dependencies
        exit /b 1
    )
) else (
    echo [WARNING] package.json not found, skipping npm install
)

REM Build TypeScript
echo [INFO] Building TypeScript...
if exist "main.ts" (
    where tsc >nul 2>&1
    if not errorlevel 1 (
        tsc main.ts --outDir dist --target es2020 --module commonjs
        if errorlevel 1 (
            echo [ERROR] TypeScript build failed
            exit /b 1
        )
        echo [INFO] TypeScript build completed
    ) else (
        echo [WARNING] TypeScript compiler not found, skipping TypeScript build
    )
) else (
    echo [WARNING] main.ts not found, skipping TypeScript build
)

REM Copy static files
echo [INFO] Copying static files...
if exist "style.css" (
    copy "style.css" "static\css\" >nul
    echo [INFO] Copied style.css to static\css\
)

if exist "script.js" (
    copy "script.js" "static\js\" >nul
    echo [INFO] Copied script.js to static\js\
)

if exist "index.html" (
    copy "index.html" "templates\" >nul
    echo [INFO] Copied index.html to templates\
)

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies
        exit /b 1
    )
    echo [INFO] Python dependencies installed
) else (
    echo [WARNING] requirements.txt not found, skipping Python dependency installation
)

REM Run Python syntax check
echo [INFO] Checking Python syntax...
set python_files=app.py run.py n8n_workflow_research.py enhance_workflow_output.py

for %%f in (%python_files%) do (
    if exist "%%f" (
        python -m py_compile "%%f"
        if errorlevel 1 (
            echo [ERROR] ✗ %%f syntax check failed
            exit /b 1
        ) else (
            echo [INFO] ✓ %%f syntax check passed
        )
    ) else (
        echo [WARNING] %%f not found, skipping syntax check
    )
)

REM Test Flask app import
echo [INFO] Testing Flask application...
if exist "app.py" (
    python -c "from app import app; print('Flask app import successful')"
    if errorlevel 1 (
        echo [ERROR] ✗ Flask application import test failed
        exit /b 1
    ) else (
        echo [INFO] ✓ Flask application import test passed
    )
)

REM Generate build info
echo [INFO] Generating build information...
echo { > build_info.json
echo     "build_date": "%date% %time%", >> build_info.json
echo     "build_version": "1.0.0", >> build_info.json
echo     "build_platform": "Windows", >> build_info.json
echo     "node_version": "$(node --version 2>nul || echo 'not available')", >> build_info.json
echo     "python_version": "$(python --version 2>nul || echo 'not available')" >> build_info.json
echo } >> build_info.json

echo [INFO] Build information saved to build_info.json

echo [INFO] 🎉 Build completed successfully!
echo [INFO] To run the application:
echo [INFO]   Development: python run.py
echo [INFO]   Production: gunicorn -w 4 -b 0.0.0.0:5000 app:app

echo ✅ Build process completed!
pause