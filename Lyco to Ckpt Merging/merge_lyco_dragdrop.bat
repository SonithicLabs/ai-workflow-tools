@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ====== CONFIG: hard-wire your Kohya venv Python ======
set "PYEXE=A:\ai_tools\kohya_ss\venv\Scripts\python.exe"
if not exist "%PYEXE%" (
  echo [ERROR] Python not found at: %PYEXE%
  pause
  exit /b 1
)

REM ====== Paths to Kohya tools (adjust if your layout differs) ======
set "LYCORIS_MERGER=A:\AI_Tools\kohya_ss\LyCORIS\tools\merge_lora.py"
set "SDSCRIPTS_MERGER=A:\ai_tools\kohya_ss\sd-scripts\networks\merge_lora.py"

REM ====== Require two drag-and-drop args ======
if "%~2"=="" (
  echo.
  echo Drag TWO items onto this .bat:
  echo   1^) BASE checkpoint  ^(.safetensors/.ckpt OR a Diffusers folder^)
  echo   2^) LyCORIS LoRA     ^(.safetensors^)
  echo.
  pause
  exit /b 1
)

REM ----- Show and choose which is BASE -----
echo [INFO] Arg1: "%~1"
echo [INFO] Arg2: "%~2"
echo.
echo Select which argument is the BASE (checkpoint):
echo   [1] %~1
echo   [2] %~2
set /p WHICHBASE=Enter 1 or 2 [1]: 
if "%WHICHBASE%"=="" set "WHICHBASE=1"

if "%WHICHBASE%"=="1" (
  set "BASE=%~1"
  set "LYCO=%~2"
) else (
  set "BASE=%~2"
  set "LYCO=%~1"
)

REM ----- Confirm inputs -----
echo.
echo [INFO] BASE: "%BASE%"
echo [INFO] LYCO: "%LYCO%"
echo.

REM ----- Ask for weight (supports negative) -----
set /p WGT=Weight (e.g. -0.20 for negative bake, 0.55 for positive) [default=-0.20]: 
if "%WGT%"=="" set "WGT=-0.20"

REM ----- Ask for UNet-only (recommended when LoRA base is unknown) -----
set /p UNETONLY=UNet-only? (y/n) [y]: 
if /I "%UNETONLY%"=="" set "UNETONLY=y"

REM ----- Ask for precision -----
set /p DTYPE=Precision fp16/fp32/bf16 [fp16]: 
if "%DTYPE%"=="" set "DTYPE=fp16"

REM ----- Build output path next to BASE -----
for %%A in ("%BASE%") do (
  set "BASEDIR=%%~dpA"
  set "BASENAME=%%~nA"
)
for %%B in ("%LYCO%") do set "LYCONAME=%%~nB"

for /f %%i in ('powershell -command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"
set "OUTFILE=%BASEDIR%%BASENAME%_fused_%LYCONAME%_%TS%.safetensors"

echo.
echo === Merge Plan ===
echo Base:   %BASE%
echo LyCO:   %LYCO%
echo Weight: %WGT%
echo UNet:   %UNETONLY%
echo DType:  %DTYPE%
echo Out:    %OUTFILE%
echo.

REM ====== Choose merger: LyCORIS tool first, fallback to sd-scripts ======
set "UNET_FLAG="
if /I "%UNETONLY%"=="y" set "UNET_FLAG=--unet_only"

if exist "%LYCORIS_MERGER%" (
  echo [INFO] Using LyCORIS tools\merge_lora.py
  REM NOTE: Current LyCORIS tools\merge_lora.py does NOT support --unet_only.
  REM If you select UNet-only, we warn but do not pass that unsupported flag to this merger.
  if /I "%UNETONLY%"=="y" echo [WARN] LyCORIS merge_lora.py does not support --unet_only; running full merge with this tool.
  "%PYEXE%" "%LYCORIS_MERGER%" ^
    --base "%BASE%" ^
    --target "%LYCO%" ^
    --output "%OUTFILE%" ^
    --weight %WGT% ^
    --precision %DTYPE% ^
    --device cpu
  set "ERR=!ERRORLEVEL!"
) else if exist "%SDSCRIPTS_MERGER%" (
  echo [INFO] LyCORIS tool not found; falling back to sd-scripts\networks\merge_lora.py
  REM sd-scripts flags: --model --lora --save_to --alpha --sdxl [--unet_only]
  REM We assume SDXL/PDXL family here; remove --sdxl if your base is SD1/SD2
  "%PYEXE%" "%SDSCRIPTS_MERGER%" ^
    --model "%BASE%" ^
    --lora  "%LYCO%" ^
    --save_to "%OUTFILE%" ^
    --alpha %WGT% ^
    --sdxl %UNET_FLAG% ^
    --save_precision %DTYPE% ^
    --device cpu
  set "ERR=!ERRORLEVEL!"
) else (
  echo [ERROR] Neither merger found:
  echo   %LYCORIS_MERGER%
  echo   %SDSCRIPTS_MERGER%
  set "ERR=1"
)

echo.
if NOT "%ERR%"=="0" (
  echo [ERROR] Merge failed. See messages above.
  pause
  exit /b 1
)

echo [DONE] Merged file:
echo   %OUTFILE%
echo.
pause
