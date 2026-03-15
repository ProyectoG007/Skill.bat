# Manual de Usuario - La Orga

## ¿Qué es La Orga?

Sistema automatizado para organizar y gestionar Skills/MCPs de AI Agents.

## Flujo de Trabajo

```
ZIP arrives → 000.A_Definir/ → procesar.bat → 
→ clasifica → numera → actualiza índice
```

## Paso a Paso

### 1. Agregar un Nuevo Skill

1. Descargar el ZIP del skill
2. Descomprimir en la carpeta `000.A_Definir/`
   - **Importante:** El contenido debe estar directamente en `000.A_Definir/`, no en una subcarpeta
3. Ejecutar `procesar.bat` (doble click)
4. El sistema:
   - Clasifica el skill en la categoría correcta
   - Lo numera (01, 02, 03...)
   - Actualiza el índice automáticamente

### 2. Verificar el Resultado

- El skill aparece en su categoría correspondiente
- El índice `indice_carpetas.md` se actualiza con la descripción
- `INDICE_SKILLS.md` en raíz muestra todos los skills

### 3. Búsqueda de Skills

Para encontrar un skill:
1. Abrir `INDICE_SKILLS.md`
2. Buscar por nombre o categoría
3. Navegar a la carpeta correspondiente

## Preguntas Frecuentes

### ¿Qué pasa si no se clasifica correctamente?

El skill irá a `000.A_Definir/`. Podés:
- Modificar el nombre del folder para que coincida con palabras clave
- Clasificarlo manualmente moviendo la carpeta

### ¿Cómo funciona la clasificación automática?

El script busca palabras clave en el nombre:
- "telegram", "discord" → API_Services
- "marketing", "content" → Marketing_Sales
- "trading", "stock" → Trading_Finance
- etc.

### ¿Puedo agregar más categorías?

Sí, editando `CATEGORIAS` en `generar_indice.py`

### ¿El proceso crea un webhook?

Opcional. Configurar variables de entorno:
```bash
set WEBHOOK_URL=https://...
set WEBHOOK_TOKEN=...
```

## Estructura de Carpetas

```
000.A_Definir/           ← Skills sin clasificar
00.Workflow_SYSTEM/      ← Sistema
  ├── generar_indice.py   ← Core del procesamiento
  ├── procesar.bat       ← Ejecutable
  ├── README.md          ← Este archivo
  └── indice_carpetas.md ← Índice generado
01_API_Services/        ← Skills de APIs
02_Marketing_Sales/     ← Skills de Marketing
...
17_SQL/                 ← Skills de SQL
```

## Solución de Problemas

### "No hay carpetas nuevas para procesar"

- Verificar que la carpeta esté en `000.A_Definir/`
- Verificar que no tenga número al inicio (ej: "01.mi-skill")
- Verificar que no sea una carpeta oculta (empezando con .)

### Error al ejecutar .bat

- Asegurarse de tener Python instalado
- Ejecutar como administrador si hay problemas de permisos

## Contacto

Para soporte o sugerencias, crear un issue en GitHub.
