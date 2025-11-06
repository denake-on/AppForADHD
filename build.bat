@echo off
echo ============================================
echo AppForADHD Build Script
echo ============================================
echo.

REM 1. Kill any running AppForADHD processes
echo [1/6] Checking for running processes...
tasklist | find /i "AppForADHD.exe" >nul
if %errorlevel% equ 0 (
    echo Found running AppForADHD.exe, terminating...
    taskkill /F /IM AppForADHD.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo Process terminated!
) else (
    echo No running processes found.
)
echo.

REM 2. Clean old build files
echo [2/6] Cleaning old files...
if exist build (
    echo Removing build directory...
    rmdir /s /q build 2>nul
    if exist build (
        echo Warning: Could not remove build directory completely
    )
)
if exist dist (
    echo Removing dist directory...
    rmdir /s /q dist 2>nul
    if exist dist (
        echo Warning: Could not remove dist directory completely
        echo Trying to force delete...
        timeout /t 2 /nobreak >nul
        rmdir /s /q dist 2>nul
    )
)
echo Done!
echo.

REM 3. Check frontend build
echo [3/6] Checking frontend build...
if not exist "frontend\dist\index.html" (
    echo Error: Frontend not built. Please run: cd frontend ^&^& npm run build
    pause
    exit /b 1
)
echo Frontend build exists!
echo.

REM 4. Check configuration files
echo [4/6] Checking configuration files...
if not exist "config.json" (
    echo Error: config.json not found
    pause
    exit /b 1
)
if not exist "backend\data\greetings.json" (
    echo Error: greetings.json not found
    pause
    exit /b 1
)
if not exist "backend\data\database.db" (
    echo Warning: database.db not found (may be first run)
)
echo Configuration files check completed!
echo.

REM 5. Execute packaging
echo [5/6] Starting packaging...
pyinstaller build_config.spec
if errorlevel 1 (
    echo Error: Packaging failed
    pause
    exit /b 1
)
echo Packaging completed!
echo.

REM 6. Verify packaging result
echo [6/6] Verifying packaging result...
if exist "dist\AppForADHD\AppForADHD.exe" (
    echo ============================================
    echo Packaging successful!
    echo Program location: dist\AppForADHD\AppForADHD.exe
    echo ============================================
    echo.
    choice /C YN /M "Do you want to test run the application now?"
    if errorlevel 2 (
        echo Skipping test run.
        echo You can run it manually from: dist\AppForADHD\AppForADHD.exe
        pause
        exit /b 0
    )
    echo Starting application...
    cd dist\AppForADHD
    start AppForADHD.exe
    echo Application started!
) else (
    echo Error: Executable file not found
    pause
    exit /b 1
)