@echo off
echo ========================================
echo Store POS Android Build Setup
echo ========================================
echo.

echo This script will help you set up Android building for your Kivy app.
echo.

echo Option 1: Install WSL (Recommended)
echo -----------------------------------
echo 1. Run this command as Administrator in PowerShell:
echo    wsl --install -d Ubuntu
echo.
echo 2. After WSL is installed and you've set up Ubuntu:
echo    - Copy your project files to WSL
echo    - Run the setup_wsl_buildozer.sh script
echo.

echo Option 2: Use Docker
echo -------------------
echo 1. Install Docker Desktop for Windows
echo 2. Run: docker pull kivy/buildozer
echo 3. Build APK: docker run --rm -v %CD%:/app kivy/buildozer android debug
echo.

echo Option 3: Use GitHub Actions (Cloud Build)
echo ------------------------------------------
echo 1. Push your code to GitHub
echo 2. The .github/workflows/build-android.yml will automatically build your APK
echo 3. Download the APK from the Actions artifacts
echo.

echo Current project is ready with:
echo - buildozer.spec configured
echo - All dependencies specified
echo - Android permissions set
echo.

echo Choose your preferred method and follow the ANDROID_PACKAGING_GUIDE.md
echo.
pause
