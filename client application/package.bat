@echo off
echo ---------------------------------------------------
echo Please wait this operation might take a few minutes
setlocal enabledelayedexpansion


REM Try to get the Python path
for /f "delims=" %%i in ('where python') do set "pythonPath=%%i"

REM Check if Python path is found
if not defined pythonPath (
    echo Python not found! Please make sure Python is installed and added to the system PATH.
    exit /b 1
) else (
    echo Python is installed at: %pythonPath%
    set PYTHON_PATH=%pythonPath%
)


set VENV_NAME=taskmasterprovenv

set SCRIPT_NAME=main.py

set EXE_NAME=TaskMasterPro.exe

set ICON_PATH="%~dp0icons\taskmasterpro.ico"

%PYTHON_PATH% -m venv !VENV_NAME!

call !VENV_NAME!\Scripts\activate

REM Install dependencies from requirements.txt
if exist requirements.txt (
    call !VENV_NAME!\Scripts\pip install -r requirements.txt
)

REM Install PyInstaller in the virtual environment
call !VENV_NAME!\Scripts\pip install pyinstaller

REM Create PyInstaller executable with specified .exe name
call !VENV_NAME!\Scripts\pyinstaller --name=!EXE_NAME! --icon=!ICON_PATH! !SCRIPT_NAME!

xcopy /s /i background dist\!EXE_NAME!\background\
xcopy /s /i icons dist\!EXE_NAME!\icons\

attrib +h "dist\!EXE_NAME!\_internal"

move "dist\!EXE_NAME!" .
ren "!EXE_NAME!" "packaged_application"
rmdir /s /q "build"
rmdir /s /q "dist"

echo PyInstaller executable generated: packaged_application\!EXE_NAME!

echo You can close this terminal.
pause