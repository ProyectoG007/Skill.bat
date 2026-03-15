import os
import re

os.chdir("scripts")

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
        "wed",
        "remotion",
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
    "11_Home_IoT": ["home", "homekit", "iot", "smart", "home-assistant"],
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
}

EXCLUIDAS = (
    ["scripts", "sala_de_juegos", "000.A_Definir"]
    + list(CATEGORIAS.keys())
    + ["__pycache__", ".ruff_cache", ".git"]
)


def clasificar(nombre):
    nombre_lower = nombre.lower()
    for cat, keywords in CATEGORIAS.items():
        for kw in keywords:
            if kw in nombre_lower:
                return cat

    palabras = re.findall(r"[a-zA-Z]+", nombre_lower)
    for palabra in palabras:
        if len(palabra) >= 2:
            return f"18_{palabra.title()}"
    return "000.A_Definir"


resultados = []

ruta_a_definir = "000.A_Definir"
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
        print(f"  Procesando {len(items)} carpetas...")
        for nombre in items:
            categoria = clasificar(nombre)
            ruta_cat = os.path.join("scripts", categoria)

            if not os.path.exists(ruta_cat):
                os.makedirs(ruta_cat)

            ruta_origen = os.path.join(ruta_a_definir, nombre)
            ruta_destino = os.path.join(ruta_cat, f"01. {nombre}")

            if os.path.exists(ruta_origen):
                os.rename(ruta_origen, ruta_destino)
                resultados.append(f"{nombre} -> {categoria}")
                print(f"    {nombre} -> {categoria}")

        with open("../resultado_proceso.txt", "w", encoding="utf-8") as f:
            f.write(f"Total: {len(resultados)}\n")
            for r in resultados:
                f.write(r + "\n")
    else:
        print("  No hay carpetas nuevas.")
        open("../resultado_proceso.txt", "w", encoding="utf-8").write("Total: 0\n")
else:
    print("  Carpeta 000.A_Definir no existe.")
    open("../resultado_proceso.txt", "w", encoding="utf-8").write("Total: 0\n")

import shutil

for cat in CATEGORIAS.keys():
    ruta_cat = os.path.join("scripts", cat)
    if os.path.exists(ruta_cat):
        items = sorted(
            [
                d
                for d in os.listdir(ruta_cat)
                if os.path.isdir(os.path.join(ruta_cat, d))
            ]
        )
        for i, item in enumerate(items, 1):
            nombre_limpio = re.sub(r"^\d+\.\s*", "", item)
            nuevo = f"{i:02d}. {nombre_limpio}"
            if item != nuevo:
                os.rename(os.path.join(ruta_cat, item), os.path.join(ruta_cat, nuevo))
