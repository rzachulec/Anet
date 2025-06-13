@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "input_dir=..\"
set "track_file=processed_files.txt"

if not exist "%track_file%" (
    type nul > "%track_file%"
)

:watch
for %%F in ("%input_dir%\*.csv") do (
    set "filename=%%~nxF"
    findstr /x /c:"!filename!" "%track_file%" >nul
    if errorlevel 1 (
        echo !filename!>>"%track_file%"
        echo Processing !filename!...
        python converter.py "..\%%~nxF"
    )
)
timeout /t 5 >nul
goto watch
