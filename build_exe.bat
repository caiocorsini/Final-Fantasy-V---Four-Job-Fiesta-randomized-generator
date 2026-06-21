@echo off
setlocal

echo Building FF5_4_Job_Fiesta executable...
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "FF5_4_Job_Fiesta" --add-data "Assets;Assets" main.py

if errorlevel 1 (
  echo.
  echo Build failed.
  exit /b 1
)

echo.
echo Build complete: dist\FF5_4_Job_Fiesta.exe
pause
