@echo off
title PhishGuard - Cyber Security Email Phishing Analyzer
color 0B
cls

echo ========================================================================
echo    PhishGuard: Email Phishing Detection & Prevention System
echo    Cyber Security Technical Club Project (C Language)
echo ========================================================================
echo.

if not exist "%~dp0phishguard.exe" (
    echo [*] Executable not found. Compiling with GCC...
    gcc -Wall -Wextra -std=c99 -I"%~dp0include" -Dstrncasecmp=_strnicmp -Dstrcasecmp=_stricmp "%~dp0src\*.c" -o "%~dp0phishguard.exe"
    if errorlevel 1 (
        echo [-] Compilation failed! Please verify GCC is installed.
        pause
        exit /b 1
    )
    echo [+] Compilation successful!
    echo.
)

:MENU
echo ------------------------------------------------------------------------
echo Choose an option to execute:
echo   [1] Scan Sample Phishing Email (PayPal Credential Theft) + Generate Reports
echo   [2] Scan Sample Spear-Phishing Email (Office 365 Account Takeover)
echo   [3] Scan Legitimate Clean Email (GitHub Token Alert)
echo   [4] Launch Interactive Assessment Mode (Live Custom Input)
echo   [5] Open Generated HTML Quarantine Security Warning in Browser
echo   [6] Recompile Source Code
echo   [7] Exit
echo ------------------------------------------------------------------------
set /p choice="Enter choice (1-7): "

if "%choice%"=="1" goto SCAN_PAYPAL
if "%choice%"=="2" goto SCAN_O365
if "%choice%"=="3" goto SCAN_GITHUB
if "%choice%"=="4" goto INTERACTIVE
if "%choice%"=="5" goto OPEN_HTML
if "%choice%"=="6" goto RECOMPILE
if "%choice%"=="7" exit /b 0

echo Invalid choice! Please select 1-7.
goto MENU

:SCAN_PAYPAL
cls
echo [*] Analyzing samples\phishing_paypal.eml...
"%~dp0phishguard.exe" "%~dp0samples\phishing_paypal.eml" --html "%~dp0quarantine.html" --json "%~dp0report.json"
echo.
pause
goto MENU

:SCAN_O365
cls
echo [*] Analyzing samples\phishing_office365.eml...
"%~dp0phishguard.exe" "%~dp0samples\phishing_office365.eml" --html "%~dp0quarantine.html" --json "%~dp0report.json"
echo.
pause
goto MENU

:SCAN_GITHUB
cls
echo [*] Analyzing samples\legitimate_github.eml...
"%~dp0phishguard.exe" "%~dp0samples\legitimate_github.eml"
echo.
pause
goto MENU

:INTERACTIVE
cls
"%~dp0phishguard.exe" --interactive
echo.
pause
goto MENU

:OPEN_HTML
if exist "%~dp0quarantine.html" (
    start "" "%~dp0quarantine.html"
    echo [+] Opened quarantine.html in default browser!
) else (
    echo [-] quarantine.html not generated yet. Run Option [1] or [2] first.
)
echo.
pause
goto MENU

:RECOMPILE
cls
echo [*] Recompiling PhishGuard...
gcc -Wall -Wextra -std=c99 -I"%~dp0include" -Dstrncasecmp=_strnicmp -Dstrcasecmp=_stricmp "%~dp0src\*.c" -o "%~dp0phishguard.exe"
if errorlevel 1 (
    echo [-] Compilation errors encountered.
) else (
    echo [+] Build succeeded! phishguard.exe updated.
)
echo.
pause
goto MENU
