@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   LA ORGA - PROCESAMIENTO DE CARPETAS
echo ========================================
echo.

echo [1/4] Descomprimiendo ZIPs en 000.A_Definir...
python "scripts\descomprimir.py"

echo.
echo [2/4] Clasificando carpetas nuevas...
python "scripts\clasificar.py"

echo.
echo [3/4] Actualizando indice...
python "scripts\actualizar_indice.py"

echo.
echo [4/4] RESULTADO:
python "scripts\mostrar_resultado.py"

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
pause
