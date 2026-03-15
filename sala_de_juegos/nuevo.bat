@echo off
chcp 65001 >nul

set "SALA_DE_JUEGOS=%~dp0"
set "SCRIPTS=%~dp0..\scripts"

:main
cls
echo ========================================
echo    SALA DE JUEGOS - La Orga
echo ========================================
echo.
echo Elegi CATEGORIA:
echo.
echo  [1] 01_API_Services
echo  [2] 02_Marketing_Sales
echo  [3] 03_Trading_Finance
echo  [4] 04_AI_ML
echo  [5] 05_Dev_Tools
echo  [6] 06_Video_Audio
echo  [7] 07_Design_Creative
echo  [8] 08_Automation
echo  [9] 09_OCR_Docs
echo [10] 10_Security
echo [11] 11_Home_IoT
echo [12] 12_Research
echo [13] 13_Browser_Agents
echo [14] 15_Obsidian
echo [15] 16_Prompt_Engineering
echo [16] 17_SQL
echo.
echo  [0] Salir
echo.

set /p CATEG="Categoria: "

if "%CATEG%"=="0" exit /b 0
if "%CATEG%"=="1" set CARPETA=01_API_Services
if "%CATEG%"=="2" set CARPETA=02_Marketing_Sales
if "%CATEG%"=="3" set CARPETA=03_Trading_Finance
if "%CATEG%"=="4" set CARPETA=04_AI_ML
if "%CATEG%"=="5" set CARPETA=05_Dev_Tools
if "%CATEG%"=="6" set CARPETA=06_Video_Audio
if "%CATEG%"=="7" set CARPETA=07_Design_Creative
if "%CATEG%"=="8" set CARPETA=08_Automation
if "%CATEG%"=="9" set CARPETA=09_OCR_Docs
if "%CATEG%"=="10" set CARPETA=10_Security
if "%CATEG%"=="11" set CARPETA=11_Home_IoT
if "%CATEG%"=="12" set CARPETA=12_Research
if "%CATEG%"=="13" set CARPETA=13_Browser_Agents
if "%CATEG%"=="14" set CARPETA=15_Obsidian
if "%CATEG%"=="15" set CARPETA=16_Prompt_Engineering
if "%CATEG%"=="16" set CARPETA=17_SQL

if not defined CARPETA goto main

:elegir_skill
cls
echo ========================================
echo    %CARPETA%
echo ========================================
echo.
echo Skills disponibles:
echo.

setlocal EnableDelayedExpansion
set CONT=0

for /f "delims=" %%a in ('dir /b "%SCRIPTS%\%CARPETA%"') do (
    set /a CONT+=1
    echo [!CONT!] %%a
)

echo.
echo  [0] Volver
echo.

endlocal

set /p NUM="Elegi skill (numero): "

if "%NUM%"=="0" goto main

setlocal EnableDelayedExpansion
set CONT=0
set ELEGIDO=

for /f "delims=" %%a in ('dir /b "%SCRIPTS%\%CARPETA%"') do (
    set /a CONT+=1
    if "!CONT!"=="%NUM%" set ELEGIDO=%%a
)

if "%ELEGIDO%"=="" (
    endlocal
    echo Skill no valido
    timeout /t 2 >nul
    goto elegir_skill
)

set SKILL=%ELEGIDO%
endlocal

:copiar
set "ORIGEN=%SCRIPTS%\%CARPETA%\%SKILL%"
set "DESTINO=%SALA_DE_JUEGOS%\%SKILL%"

if exist "%DESTINO%" (
    echo.
    echo Ya existe! Usando carpeta existente.
) else (
    xcopy /e /i /y "%ORIGEN%" "%DESTINO%" >nul 2>&1
    echo.
    echo Copiado a: %DESTINO%
)

:menu
cls
echo ========================================
echo    %SKILL%
echo ========================================
echo.

if exist "%DESTINO%\package.json" (
    echo Tipo: Node.js
) else if exist "%DESTINO%\requirements.txt" (
    echo Tipo: Python
) else (
    echo Tipo: Documentacion
)

echo.
echo [1] Ver estructura
echo [2] Abrir SKILL.md
echo [3] Instalar dependencias
echo [4] Copiar ruta
echo [5] Elegir otro
echo [0] Salir
echo.

set /p OPCION="Opcion: "

if "%OPCION%"=="1" goto estructura
if "%OPCION%"=="2" goto abrir
if "%OPCION%"=="3" goto instalar
if "%OPCION%"=="4" goto ruta
if "%OPCION%"=="5" goto main
if "%OPCION%"=="0" exit /b 0

goto menu

:estructura
cls
dir /s /b "%DESTINO%"
echo.
pause
goto menu

:abrir
if exist "%DESTINO%\SKILL.md" (
    start "" "%DESTINO%\SKILL.md"
) else (
    echo No existe SKILL.md
    timeout /t 2 >nul
)
goto menu

:instalar
cd /d "%DESTINO%"
if exist "package.json" (
    echo Ejecutando npm install...
    npm install
    pause
) else if exist "requirements.txt" (
    echo Ejecutando pip install -r requirements.txt...
    pip install -r requirements.txt
    pause
) else (
    echo No hay dependencias
    timeout /t 2 >nul
)
goto menu

:ruta
echo %DESTINO% | clip
echo Ruta copiada!
timeout /t 1 >nul
goto menu
