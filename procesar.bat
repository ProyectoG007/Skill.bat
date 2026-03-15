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
python -c "
import os
import re
import json

os.chdir('scripts')

EXCLUIDAS = ['scripts', 'sala_de_juegos', '000.A_Definir']

CATEGORIAS = {
    '01_API_Services': ['api', 'gateway', 'discord', 'telegram', 'google', 'notion', 'whisper', 'qveris', 'drive', 'meet', 'play'],
    '02_Marketing_Sales': ['marketing', 'sales', 'content', 'ad', 'adclaw', 'productivity', 'market', 'hzl', 'data-analysis'],
    '03_Trading_Finance': ['trading', 'finance', 'stock', 'risk', 'tushare', 'investment'],
    '04_AI_ML': ['ai', 'ml', 'machine-learning', 'humanizer', 'memory', 'self-improving', 'senior-ml'],
    '05_Dev_Tools': ['dev', 'tool', 'git', 'github', 'gitlab', 'docker', 'cursor', 'playwright', 'tdd', 'mcporter', 'code'],
    '06_Video_Audio': ['video', 'audio', 'transcript', 'subtitle', 'youtube', 'fathom', 'retake', 'wed', 'remotion'],
    '07_Design_Creative': ['design', 'creative', 'ppt', 'powerpoint', 'beauty', 'frontend', 'nano-banana', 'superdesign'],
    '08_Automation': ['automation', 'auto', 'n8n', 'command-center', 'computer-use', 'fast-', 'browser', 'screenshot', 'proactive'],
    '09_OCR_Docs': ['ocr', 'excel', 'xlsx', 'document', 'pdf', 'paddleocr', 'doc'],
    '10_Security': ['security', 'secure', 'clawsec', 'moltguard', 'verified', 'identity', 'audit'],
    '11_Home_IoT': ['home', 'homekit', 'iot', 'smart', 'home-assistant'],
    '12_Research': ['research', 'academic', 'reflection', 'guide', 'content-id'],
    '13_Browser_Agents': ['browser', 'agent', 'clawdbot', 'commerce', 'orchestration', 'architect'],
    '14_Oracle_DB': ['oracle', 'database', 'db'],
    '15_Obsidian': ['obsidian', 'vault'],
    '16_Prompt_Engineering': ['prompt', 'engineering'],
    '17_SQL': ['sql', 'query'],
}

CATEGORIAS.update({f'0{i}_AI_ML': [] for i in range(18, 100)})

EXCLUIDAS += list(CATEGORIAS.keys()) + ['__pycache__', '.ruff_cache', '.git']

ruta_a_definir = '000.A_Definir'
resultados = []

if os.path.exists(ruta_a_definir):
    items = [d for d in os.listdir(ruta_a_definir) if os.path.isdir(os.path.join(ruta_a_definir, d)) and not re.match(r'^\d+\.', d) and not d.startswith('.') and d not in EXCLUIDAS]
    
    if items:
        print(f'  Procesando {len(items)} carpetas...')
        for nombre in items:
            nombre_lower = nombre.lower()
            categoria = '000.A_Definir'
            
            for cat, keywords in CATEGORIAS.items():
                for kw in keywords:
                    if kw in nombre_lower:
                        categoria = cat
                        break
                if categoria != '000.A_Definir':
                    break
            
            if categoria == '000.A_Definir':
                palabras = re.findall(r'[a-zA-Z]+', nombre_lower)
                for palabra in palabras:
                    if len(palabra) >= 2:
                        categoria = f'18_{palabra.title()}'
                        break
            
            resultados.append(f'{nombre} -> {categoria}')
            print(f'    {nombre} -> {categoria}')

if resultados:
    with open('../proceso_log.txt', 'w', encoding='utf-8') as f:
        f.write(f'Total procesados: {len(resultados)}\n')
        for r in resultados:
            f.write(r + '\n')
else:
    with open('../proceso_log.txt', 'w', encoding='utf-8') as f:
        f.write('Total procesados: 0\n')
print('  Proceso guardado.')
"

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
echo [4/4] RESULTADO DEL PROCESO:
echo ========================================
if exist proceso_log.txt (
    type proceso_log.txt
    del proceso_log.txt
) else (
    echo   No se procesaron carpetas nuevas.
)
echo ========================================

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
pause
