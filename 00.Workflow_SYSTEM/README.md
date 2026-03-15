# LA ORGA - Workflow SYSTEM

Sistema de organización automática de Skills/MCPs.

## Estructura

```
MarkDown/
├── 000.A_Definir/        ← Skills nuevos sin clasificar
├── 00.Workflow_SYSTEM/   ← Scripts y archivos del sistema
├── 01_API_Services/      ← APIs externas (Discord, Telegram, Google, etc.)
├── 02_Marketing_Sales/   ← Marketing y ventas
├── 03_Trading_Finance/    ← Trading y finanzas
├── 04_AI_ML/            ← AI y Machine Learning
├── 05_Dev_Tools/        ← Herramientas de desarrollo
├── 06_Video_Audio/      ← Video y audio
├── 07_Design_Creative/  ← Diseño y creatividad
├── 08_Automation/       ← Automatización
├── 09_OCR_Docs/         ← OCR y documentos
├── 10_Security/         ← Seguridad
├── 11_Home_IoT/         ← HomeKit y IoT
├── 12_Research/         ← Investigación
├── 13_Browser_Agents/   ← Agentes de navegador
├── 14_Oracle_DB/        ← Oracle Database
├── 15_Obsidian/         ← Obsidian
├── 16_Prompt_Engineering/ ← Prompt Engineering
└── 17_SQL/              ← SQL
```

## Uso

### 1. Agregar nuevos Skills
1. Descomprimir ZIP en `000.A_Definir/`
2. Ejecutar `procesar.bat` (doble click)
3. El script clasificará automáticamente

### 2. Proceso manual
```
Doble click en: 00.Workflow_SYSTEM\procesar.bat
```

### 3. Scripts disponibles
- `generar_indice.py` - Numera carpetas y genera índice
- `procesar.bat` - Proceso completo (incluye clasificación)
- `descomprimir.py` - Descomprime ZIPs

## Workflow

```
ZIP arrives → 000.A_Definir/ → ejecutar procesar.bat → 
→ clasifica en categoría → numera → actualiza índice
```

## Notas
- Carpetas ocultas (empezando con .) se ignoran
- Se extrae descripción de _meta.json, package.json, skill.json
- El índice se guarda en `00.Workflow_SYSTEM/indice_carpetas.md`
