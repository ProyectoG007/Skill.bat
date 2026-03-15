---
nombre: generador-visual-pdf
versión: 1.0.0
descripción: "Transforma texto plano en un PDF profesional con diseño visual, emojis, colores y gráficos. Usar cuando el usuario quiere un PDF entregable estético desde contenido sin formato."
Licencia: MIT
autor: "Nicolás Neira"
Página principal: https://nicolasneira.com/docs/claude-agent-teams/
metadatos:
  categoría: productividad
  etiquetas:
    - pdf
    - impresión fácil
    - html
    - diseño visual
herramientas permitidas:
  - Golpe
  - Escribir
---

# Generador visual de PDF

## Instrucciones

1. Recibir texto plano del usuario
2. Generar archivo HTML+CSS con diseño visual profesional
3. Convertir un PDF con WeasyPrint

## Instalación

``golpe
pip install weasyprint
```

Dependencias del sistema:
- macOS: `brew install pango cairo libffi`
- Linux: `apt-get install libpango-1.0-0 libpangocairo-1.0-0 libcairo2`

## Diseño HTML+CSS

Generar HTML completo con CSS embebido. Usar `lang="es"` en `<html>` para habilitar `hyphens: auto`.

### CSS permitido

- **Diseño:** flexbox, cuadrícula básica (sin auto-fill/fit, sin subcuadrículas)
- **Colores:** linear-gradient(), radial-gradient() como background-image
- **Tipografía:** @font-face, variantes de fuente, variables CSS con var()
- **Bordes:** radio de borde, múltiples fondos
- **Paginación:** @page, break-before, break-after, break-inside, orphans, widows

### CSS prohibido

| Propiedad | Alternativa |
|-----------|-------------|
| sombra de caja | borde o contorno con color sólido |
| cálculo() | Calcular el valor manualmente y escribirlo directo |
| vw, vh, vmín, vmáx | Usar mm, cm o px |
| transformaciones 3D | No disponible |
| :hover, :activo, :enfoque | Ignorados en PDF |

### Paleta de colores

Adaptar al contexto del usuario. Sin indicación, usar paleta corporativa neutra (azules/grises). Si menciona marca, adapte a sus colores. Definir con variables CSS en `:root`. Usar gradientes para encabezados y secciones destacadas.

## PaginaciÃ³n

```css
@página {
  Tamaño: A4;
  margen: 20 mm 15 mm 25 mm 15 mm;
}

@page :first {
  margen superior: 0;
}

.sección {
  break-inside: evitar;
}

.salto de página {
  break-before: página;
}
```

## Emojis

WeasyPrint renderiza emojis si el sistema tiene fuente de emojis.

- Linux: `apt-get install fonts-noto-color-emoji`
- macOS: Apple Color Emoji ya disponible

Insertar directamente en HTML. Si no renderizan, ofrecemos reemplazar con iconos SVG en línea.

## Gráficas

Generar SVG en línea en HTML. WeasyPrint renderiza SVG como vector.

- **Barras:** para comparaciones. Usar `<rect>` con etiquetas `<text>`.
- **Donut:** para proporciones. Usar `<circle>` con Stroke-dasharray.
- **Líneas:** para tendencias. Usar `<polilínea>`.

Calcular posiciones a partir de los datos del usuario. Siempre incluya etiquetas de texto. Si los datos no son claros para gráfica, use tabla estilizada.

## Imágenes

- Preferir URI base64/data para imágenes embebidas
- Las URL externas tienen un tiempo de espera de 10 segundos. Ajustar con `--timeout`
- Formatos: PNG, JPEG, GIF, WebP, SVG

## Conversión a PDF

``golpe
weasyprint <HTML_ENTRADA> <ARCHIVO_SALIDA>
```

Banderas Ãºtiles:

``golpe
# Con hoja de estilos adicionales
weasyprint <HTML_ENTRADA> <ARCHIVO_SALIDA> -s <HOJA_DE_ESTILO>

# Optimizar imágenes (reducir tamaño del PDF)
weasyprint <HTML_ENTRADA> <ARCHIVO_SALIDA> --optimizar-imágenes -j 85

# Resolver rutas relativas
weasyprint <HTML_ENTRADA> <ARCHIVO_SALIDA> -u <URL_BASE>

# Cambiar resolución
weasyprint <HTML_ENTRADA> <ARCHIVO_SALIDA> -r 150
```

## Decisiones

- **Tamaño de página:** A4 por defecto. Letter si el usuario lo solicita o el contexto es US.
- **Diseño:** Flexbox por defecto. Grid solo para diseños de tarjetas simples (2-3 columnas).

## Errores comunes

### `OSError: no se encontró ninguna biblioteca llamada "pango"/"cairo"`
Instalar dependencias del sistema (ver sección Instalación).

### PDF con texto cortado o desbordado
Agregar `break-inside: evitar` a las secciones. Dividir contenido largo con `break-before: page`.

### Imágenes externas no aparecen
Tiempo de espera agotado o URL inaccesible. Convertir a base64 inline o usar `--timeout 30`.

### Fuentes no se embeben correctamente
WeasyPrint subsetea fuentes automáticamente. Para incluir todas las variantes, use la API Python con `font_config` y cargue las fuentes explícitamente:
```python
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

configuración_de_fuente = Configuración_de_fuente()
HTML(string=html_content).write_pdf('<OUTPUT_FILE>', font_config=font_config)
```

## Referencias
- [Documentación de WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/)
- [Soporte CSS de WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/api_reference.html)