import os
import re
import json
import glob
import requests
from datetime import datetime

MAX_FILE_SIZE = 1024 * 1024


def obtener_descripcion_json(ruta_carpeta):
    archivos_json = [
        "package.json",
        "manifest.json",
        "config.json",
        "skill.json",
        "metadata.json",
    ]
    for nombre in archivos_json:
        ruta = os.path.join(ruta_carpeta, nombre)
        if os.path.exists(ruta):
            try:
                if os.path.getsize(ruta) > MAX_FILE_SIZE:
                    continue
                with open(ruta, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("description") or data.get("name") or None
            except:
                continue
    return None


def obtener_descripcion_python(ruta_carpeta):
    archivos_py_prioritarios = []

    nombre_carpeta = os.path.basename(ruta_carpeta)
    for f in os.listdir(ruta_carpeta):
        if f.endswith(".py"):
            if f.lower() in ["main.py", "app.py", f"{nombre_carpeta}.py"]:
                archivos_py_prioritarios.insert(0, f)
            else:
                archivos_py_prioritarios.append(f)

    for archivo in archivos_py_prioritarios[:3]:
        ruta = os.path.join(ruta_carpeta, archivo)
        try:
            if os.path.getsize(ruta) > MAX_FILE_SIZE:
                continue
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = [f.readline() for _ in range(10)]
                contenido = "".join(lineas)

                docstring_triple = re.search(r'"""(.*?)"""', contenido, re.DOTALL)
                if docstring_triple:
                    texto = docstring_triple.group(1).strip().split("\n")[0]
                    return texto[:100] if texto else None

                docstring_simple = re.search(r"'''(.*?)'''", contenido, re.DOTALL)
                if docstring_simple:
                    texto = docstring_simple.group(1).strip().split("\n")[0]
                    return texto[:100] if texto else None

                for linea in lineas:
                    match = re.match(r"^#\s*(.+)", linea)
                    if match:
                        return match.group(1).strip()[:100]
        except:
            continue
    return None


def analizar_contenido(ruta_carpeta):
    desc_json = obtener_descripcion_json(ruta_carpeta)
    if desc_json:
        return desc_json

    desc_py = obtener_descripcion_python(ruta_carpeta)
    if desc_py:
        return desc_py

    try:
        archivos = os.listdir(ruta_carpeta)
        if not archivos:
            return "Carpeta vacía"

        for nombre in archivos:
            if nombre.lower() in [
                "readme.md",
                "leeme.txt",
                "notas.txt",
            ] or nombre.endswith(".md"):
                ruta = os.path.join(ruta_carpeta, nombre)
                try:
                    if os.path.getsize(ruta) > MAX_FILE_SIZE:
                        continue
                    with open(ruta, "r", encoding="utf-8") as f:
                        linea = f.readline().strip()
                        if linea:
                            return re.sub(r"[#*`]", "", linea)[:100]
                except:
                    continue

        extensiones = set(
            os.path.splitext(f)[1]
            for f in archivos
            if os.path.isfile(os.path.join(ruta_carpeta, f))
        )
        if extensiones:
            return f"Contiene archivos: {', '.join(list(extensiones)[:3])}"
        return "Contiene subcarpetas u otros elementos."
    except Exception:
        return "No se pudo analizar el contenido."


def detectar_tecnologias(ruta_carpeta):
    extensiones = set()
    try:
        for root, dirs, files in os.walk(ruta_carpeta):
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext:
                    extensiones.add(ext)
    except:
        pass
    return sorted(list(extensiones))[:10]


def enviar_webhook(datos):
    webhook_url = os.environ.get("WEBHOOK_URL")
    webhook_token = os.environ.get("WEBHOOK_TOKEN")

    if not webhook_url:
        print("WEBHOOK_URL no configurada. Omitiendo notificación.")
        return True

    headers = {"Content-Type": "application/json"}
    if webhook_token:
        headers["Authorization"] = f"Bearer {webhook_token}"

    payload = {
        "origen": "La_Orga_Markdown",
        "accion": "indexacion_automatica",
        "data": datos,
    }

    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print("Webhook enviado exitosamente.")
            return True
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        try:
            with open("webhook_error.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] Error: {str(e)}\n")
                f.write(f"Payload: {json.dumps(payload, ensure_ascii=False)}\n\n")
            print(f"Webhook fallido. Error registrado en webhook_error.log")
        except:
            pass
        return False


CATEGORIAS = {
    "01_API_Services": [
        "api",
        "gateway",
        "discord",
        "telegram",
        "google",
        "notion",
        "whisper",
        "qveris",
        "drive",
        "meet",
        "play",
    ],
    "02_Marketing_Sales": [
        "marketing",
        "sales",
        "content",
        "ad",
        "adclaw",
        "productivity",
        "market",
        "hzl",
        "data-analysis",
    ],
    "03_Trading_Finance": [
        "trading",
        "finance",
        "stock",
        "risk",
        "tushare",
        "investment",
    ],
    "04_AI_ML": [
        "ai",
        "ml",
        "machine-learning",
        "humanizer",
        "memory",
        "self-improving",
        "senior-ml",
    ],
    "05_Dev_Tools": [
        "dev",
        "tool",
        "git",
        "github",
        "gitlab",
        "docker",
        "cursor",
        "playwright",
        "tdd",
        "mcporter",
        "code",
    ],
    "06_Video_Audio": [
        "video",
        "audio",
        "transcript",
        "subtitle",
        "youtube",
        "fathom",
        "retake",
    ],
    "07_Design_Creative": [
        "design",
        "creative",
        "ppt",
        "powerpoint",
        "beauty",
        "frontend",
        "nano-banana",
        "superdesign",
    ],
    "08_Automation": [
        "automation",
        "auto",
        "n8n",
        "command-center",
        "computer-use",
        "fast-",
        "browser",
        "screenshot",
        "proactive",
    ],
    "09_OCR_Docs": ["ocr", "excel", "xlsx", "document", "pdf", "paddleocr", "doc"],
    "10_Security": [
        "security",
        "secure",
        "clawsec",
        "moltguard",
        "verified",
        "identity",
        "audit",
    ],
    "11_Home_IoT": ["home", "homekit", "iot", "smart"],
    "12_Research": ["research", "academic", "reflection", "guide", "content-id"],
    "13_Browser_Agents": [
        "browser",
        "agent",
        "clawdbot",
        "commerce",
        "orchestration",
        "architect",
    ],
    "14_Oracle_DB": ["oracle", "database", "db"],
    "15_Obsidian": ["obsidian", "vault"],
    "16_Prompt_Engineering": ["prompt", "engineering"],
    "17_SQL": ["sql", "query"],
    "06_Video_Audio": ["video", "audio", "wed", "remotion"],
}


def clasificar_carpeta(nombre, ruta_raiz):
    nombre_lower = nombre.lower()

    # Buscar en categorías existentes
    for categoria, keywords in CATEGORIAS.items():
        for kw in keywords:
            if kw in nombre_lower:
                return categoria

    # Si no coincide, crear nueva categoría basada en palabras del nombre
    palabras = re.findall(r"[a-zA-Z]+", nombre_lower)
    for palabra in palabras:
        if len(palabra) >= 2:
            nueva_cat = f"18_{palabra.title().replace('_', '')}"
            ruta_nueva_cat = os.path.join(ruta_raiz, nueva_cat)
            if not os.path.exists(ruta_nueva_cat):
                os.makedirs(ruta_nueva_cat)
                print(f"Creada nueva categoria: {nueva_cat}")
                # Agregar al diccionario para siguientes archivos
                CATEGORIAS[nueva_cat] = [palabra]
                return nueva_cat

    return "000.A_Definir"


def renumerar_categorias(ruta_raiz):
    categorias = [
        d
        for d in os.listdir(ruta_raiz)
        if os.path.isdir(os.path.join(ruta_raiz, d))
        and (d.startswith("0") or d.startswith("1"))
        and d not in ["00.Workflow_SYSTEM", "000.A_Definir"]
    ]

    for cat in categorias:
        ruta_cat = os.path.join(ruta_raiz, cat)
        items = sorted(
            [
                d
                for d in os.listdir(ruta_cat)
                if os.path.isdir(os.path.join(ruta_cat, d))
            ]
        )

        for i, item in enumerate(items, 1):
            nombre_limpio = re.sub(r"^\d+\.\s*", "", item)
            nuevo_nombre = f"{i:02d}. {nombre_limpio}"
            ruta_vieja = os.path.join(ruta_cat, item)
            ruta_nueva = os.path.join(ruta_cat, nuevo_nombre)
            if ruta_vieja != ruta_nueva:
                os.rename(ruta_vieja, ruta_nueva)


EXCLUIDAS = (
    ["scripts", "sala_de_juegos", "000.A_Definir"]
    + list(CATEGORIAS.keys())
    + ["__pycache__", ".ruff_cache", ".git"]
)


def renumerar_categorias(ruta_raiz):
    """Renumera carpetas dentro de cada categoría"""
    categorias = [
        d
        for d in os.listdir(ruta_raiz)
        if os.path.isdir(os.path.join(ruta_raiz, d))
        and (d.startswith("0") or d.startswith("1"))
        and d not in EXCLUIDAS
    ]

    for cat in categorias:
        ruta_cat = os.path.join(ruta_raiz, cat)
        items = sorted(
            [
                d
                for d in os.listdir(ruta_cat)
                if os.path.isdir(os.path.join(ruta_cat, d))
            ]
        )

        for i, item in enumerate(items, 1):
            # Limpiar cualquier número viejo y renumerar
            nombre_limpio = re.sub(r"^\d+\.\s*", "", item)
            nuevo_nombre = f"{i:02d}. {nombre_limpio}"
            ruta_vieja = os.path.join(ruta_cat, item)
            ruta_nueva = os.path.join(ruta_cat, nuevo_nombre)
            if ruta_vieja != ruta_nueva:
                os.rename(ruta_vieja, ruta_nueva)


def organizar_y_indexar(ruta_raiz):
    try:
        os.chdir(ruta_raiz)

        # Primero buscar en 000.A_Definir
        ruta_a_definir = os.path.join(ruta_raiz, "000.A_Definir")
        items = []

        if os.path.exists(ruta_a_definir):
            items = [
                d
                for d in os.listdir(ruta_a_definir)
                if os.path.isdir(os.path.join(ruta_a_definir, d))
                and not re.match(r"^\d+\.", d)
                and not d.startswith(".")
                and d not in EXCLUIDAS
            ]
            if items:
                print(f"Procesando {len(items)} carpetas de 000.A_Definir...")

        # Si no hay en 000.A_Definir, buscar en raíz
        if not items:
            items = [
                d
                for d in os.listdir()
                if os.path.isdir(d)
                and not re.match(r"^\d+\.", d)
                and not d.startswith(".")
                and d not in EXCLUIDAS
            ]
            if items:
                print(f"Procesando {len(items)} carpetas de raíz...")

        if not items:
            print("No hay carpetas nuevas para procesar.")
            return

        print(f"Procesando {len(items)} carpetas...")

        # Determinar ruta de origen
        origen = ruta_raiz  # Default: raíz
        if os.path.exists(ruta_a_definir):
            items_a_definir = [
                d
                for d in os.listdir(ruta_a_definir)
                if os.path.isdir(os.path.join(ruta_a_definir, d))
                and not re.match(r"^\d+\.", d)
                and not d.startswith(".")
                and d not in EXCLUIDAS
            ]
            if items_a_definir:
                origen = ruta_a_definir
                items = items_a_definir

        datos_indice = []
        items_data = []

        for i, nombre_original in enumerate(items, start=1):
            numero_str = f"{i:02d}"
            nuevo_nombre = f"{numero_str}. {nombre_original}"

            ruta_antigua = os.path.join(origen, nombre_original)

            categoria = clasificar_carpeta(nombre_original, ruta_raiz)
            ruta_categoria = os.path.join(ruta_raiz, categoria)

            if not os.path.exists(ruta_categoria):
                os.makedirs(ruta_categoria)
                print(f"Creada categoría: {categoria}")

            ruta_nueva = os.path.join(ruta_categoria, nuevo_nombre)

            explicacion = analizar_contenido(ruta_antigua)
            tecnologias = detectar_tecnologias(ruta_antigua)

            os.rename(ruta_antigua, ruta_nueva)

            datos_indice.append((numero_str, nuevo_nombre, explicacion))
            items_data.append(
                {
                    "nro": numero_str,
                    "nombre_nuevo": nuevo_nombre,
                    "explicacion_tecnica": explicacion,
                    "tecnologias_detectadas": tecnologias,
                    "categoria": categoria,
                }
            )

            print(f"-> {categoria}: {nombre_original}")

        with open("indice_automatico.md", "w", encoding="utf-8") as f:
            f.write("# Reporte de Organización Automática\n\n")
            f.write("| N° | Carpeta | Explicación | Tecnologías |\n")
            f.write("|---|---|---|---|\n")
            for num, nombre, desc in datos_indice:
                tech = next(
                    (
                        item["tecnologias_detectadas"]
                        for item in items_data
                        if item["nro"] == num
                    ),
                    [],
                )
                tech_str = ", ".join(tech) if tech else "-"
                f.write(f"| {num} | **{nombre}** | {desc} | {tech_str} |\n")

        webhook_data = {"total_carpetas": len(items), "items": items_data}
        enviar_webhook(webhook_data)

        renumerar_categorias(ruta_raiz)

        print(
            "\nListo! Carpetas clasificadas, renumeradas e indice_automatico.md generado."
        )

    except Exception as e:
        print(f"Error crítico: {e}")


if __name__ == "__main__":
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz = os.path.dirname(script_dir)  # MarkDown/
    os.chdir(script_dir)  # Trabajar desde scripts/
    ruta = script_dir
    organizar_y_indexar(ruta)
