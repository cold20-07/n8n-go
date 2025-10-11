@echo off
echo 🧹 CLEANING PROJECT FOR VERCEL DEPLOYMENT
echo ==========================================

echo 🗑️  Removing Python files...
del /s /q *.py 2>nul
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /q requirements*.txt 2>nul
del /q pytest.ini 2>nul
del /q setup.py 2>nul
del /q pyproject.toml 2>nul

echo ✅ Python files removed

echo 📦 Verifying Node.js configuration...
if not exist "package.json" (
    echo ❌ package.json missing!
    exit /b 1
)

if not exist "api\index.js" (
    echo ❌ api\index.js missing!
    exit /b 1
)

if not exist "vercel.json" (
    echo ❌ vercel.json missing!
    exit /b 1
)

echo ✅ All Node.js files present

echo.
echo 🚀 PROJECT READY FOR DEPLOYMENT
echo ================================
echo ✅ Python files removed
echo ✅ Node.js configuration verified
echo ✅ Vercel configuration present
echo.
echo Deploy with:
echo vercel --prod