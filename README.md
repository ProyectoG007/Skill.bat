# LA ORGA - Sistema de Gestión de Skills/MCPs

Repositorio centralizado para organizar, clasificar y gestionar Skills de AI.

## Estructura del Proyecto

```
MarkDown/
├── 000.A_Definir/              ← Skills nuevos sin clasificar
├── 00.Workflow_SYSTEM/          ← Scripts y documentación del sistema
│   ├── generar_indice.py        ← Script de procesamiento
│   ├── procesar.bat            ← Ejecutable para procesar carpetas
│   ├── README.md               ← Documentación del sistema
│   └── indice_carpetas.md      ← Índice de skills
├── 01_API_Services/            ← APIs externas
├── 02_Marketing_Sales/         ← Marketing y ventas
├── 03_Trading_Finance/         ← Trading y finanzas
├── 04_AI_ML/                  ← AI y Machine Learning
├── 05_Dev_Tools/              ← Herramientas de desarrollo
├── 06_Video_Audio/            ← Video y audio
├── 07_Design_Creative/        ← Diseño y creatividad
├── 08_Automation/             ← Automatización
├── 09_OCR_Docs/               ← OCR y documentos
├── 10_Security/                ← Seguridad
├── 11_Home_IoT/               ← HomeKit y IoT
├── 12_Research/               ← Investigación
├── 13_Browser_Agents/         ← Agentes de navegador
├── 14_Oracle_DB/              ← Oracle Database
├── 15_Obsidian/               ← Obsidian
├── 16_Prompt_Engineering/     ← Prompt Engineering
└── 17_SQL/                    ← SQL
```

## Quick Start

### Agregar un nuevo Skill

1. **Descomprimir** el ZIP del skill en `000.A_Definir/`
2. **Ejecutar** `00.Workflow_SYSTEM\procesar.bat` (doble click)
3. **Listo** → El skill se clasifica, numera y actualiza el índice

### Búsqueda de Skills

- Consultar `INDICE_SKILLS.md` o `00.Workflow_SYSTEM/indice_carpetas.md`
- Buscar por nombre de skill o categoría

## Categorías

| Código | Categoría | Descripción |
|--------|-----------|-------------|
| 01 | API_Services | APIs externas (Discord, Telegram, Google, etc.) |
| 02 | Marketing_Sales | Marketing y ventas |
| 03 | Trading_Finance | Trading y finanzas |
| 04 | AI_ML | Inteligencia Artificial y Machine Learning |
| 05 | Dev_Tools | Herramientas de desarrollo |
| 06 | Video_Audio | Video y audio |
| 07 | Design_Creative | Diseño y creatividad |
| 08 | Automation | Automatización |
| 09 | OCR_Docs | OCR y documentos |
| 10 | Security | Seguridad |
| 11 | Home_IoT | HomeKit y IoT |
| 12 | Research | Investigación |
| 13 | Browser_Agents | Agentes de navegador |
| 14 | Oracle_DB | Oracle Database |
| 15 | Obsidian | Obsidian |
| 16 | Prompt_Engineering | Prompt Engineering |
| 17 | SQL | SQL |
| 18+ | (auto) | Categorías creadas dinámicamente |

> **Nota:** Las categorías 18+ se crean automáticamente si el skill no coincide con ninguna categoría existente.

## Configuración

### Variables de Entorno (Opcional)

```bash
# Para Webhook de notificaciones
set WEBHOOK_URL=https://tu-servidor.com/webhook
set WEBHOOK_TOKEN=tu-token-secreto
```

## Scripts Disponibles

- `generar_indice.py` - Procesa carpetas nuevas
- `procesar.bat` - Ejecuta el proceso completo
- `descomprimir.py` - Descomprime ZIPs

## Licencia

MIT
