@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   LA ORGA - PROCESAMIENTO DE CARPETAS
echo ========================================
echo.

echo [1/4] Descomprimiendo ZIPs en 000.A_Definir...
python -c "
import os
import zipfile

ruta = 'scripts/000.A_Definir'
if os.path.exists(ruta):
    os.chdir(ruta)
    archivos = [f for f in os.listdir('.') if f.endswith('.zip')]
    if archivos:
        for archivo in archivos:
            nombre_carpeta = archivo[:-4]
            try:
                print(f'  Descomprimiendo: {archivo}')
                with zipfile.ZipFile(archivo, 'r') as zip_ref:
                    os.makedirs(nombre_carpeta, exist_ok=True)
                    zip_ref.extractall(nombre_carpeta)
                os.remove(archivo)
                print(f'  Listo: {archivo} -> {nombre_carpeta}')
            except Exception as e:
                print(f'  Error: {archivo} - {e}')
    else:
        print('  No hay ZIPs para descomprimir.')
else:
    print('  Carpeta 000.A_Definir no existe.')
"

echo.
echo [2/4] Procesando carpetas nuevas...
python "scripts/generar_indice.py"

echo.
echo [3/4] Actualizando indice de carpetas...
python -c "
import os
import json
from datetime import datetime

categorias = sorted([d for d in os.listdir('scripts') if os.path.isdir(os.path.join('scripts', d)) and d.startswith(('0','1')) and d not in ['000.A_Definir']])

with open('scripts/indice_carpetas.md', 'w', encoding='utf-8') as f:
    f.write('# Indice de Carpetas - La Orga\n')
    f.write(f'# Actualizado: {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}\n\n')
    f.write('| Categoria | N | Carpeta | Descripcion |\n')
    f.write('|---|---|---|---|\n')
    for cat in categorias:
        for item in sorted(os.listdir(os.path.join('scripts', cat))):
            num = item.split('.')[0]
            desc = '---'
            for meta in ['_meta.json', 'package.json', 'skill.json', 'metadata.json']:
                ruta = os.path.join('scripts', cat, item, meta)
                if os.path.exists(ruta):
                    try:
                        with open(ruta, 'r', encoding='utf-8') as mf:
                            data = json.load(mf)
                            desc = (data.get('description') or data.get('name') or '---')[:50]
                            break
                    except: pass
            f.write(f'| {cat} | {num} | {item} | {desc} |\n')
print('Indice actualizado!')
"

echo.
echo [4/4] Resumen de carpetas por categoria:
for /d %%d in (scripts\0*) do (
    echo   %%~nd
)

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
pause
